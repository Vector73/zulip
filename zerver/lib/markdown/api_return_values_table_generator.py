import copy
import json
import re
from collections import OrderedDict
from typing import Any, Dict, List, Mapping, Optional

import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from typing_extensions import override

from zerver.lib.markdown.priorities import PREPROCESSOR_PRIORITIES
from zerver.openapi.openapi import check_deprecated_consistency, get_openapi_return_values

from .api_arguments_table_generator import generate_data_type

REGEXP = re.compile(r"\{generate_return_values_table\|\s*(.+?)\s*\|\s*(.+)\s*\}")


class MarkdownReturnValuesTableGenerator(Extension):
    @override
    def extendMarkdown(self, md: markdown.Markdown) -> None:
        md.preprocessors.register(
            APIReturnValuesTablePreprocessor(md, self.getConfigs()),
            "generate_return_values",
            PREPROCESSOR_PRIORITIES["generate_return_values"],
        )


class APIReturnValuesTablePreprocessor(Preprocessor):
    def __init__(self, md: markdown.Markdown, config: Mapping[str, Any]) -> None:
        super().__init__(md)

    @override
    def run(self, lines: List[str]) -> List[str]:
        done = False
        while not done:
            for line in lines:
                loc = lines.index(line)
                match = REGEXP.search(line)

                if not match:
                    continue

                doc_name = match.group(2)
                endpoint, method = doc_name.rsplit(":", 1)
                return_values = get_openapi_return_values(endpoint, method)
                if doc_name == "/events:get":
                    return_values = copy.deepcopy(return_values)
                    events = return_values["events"].pop("items", None)
                    text = self.render_table(return_values, 0)
                    # Another heading for the events documentation
                    text.append("\n\n## Events by `type`\n\n")
                    text += self.render_events(events)
                else:
                    text = self.render_table(return_values, 0)
                if len(text) > 0:
                    text = ["#### Return values", *text]
                line_split = REGEXP.split(line, maxsplit=0)
                preceding = line_split[0]
                following = line_split[-1]
                text = [preceding, *text, following]
                lines = lines[:loc] + text + lines[loc + 1 :]
                break
            else:
                done = True
        return lines

    def render_desc(
        self, description: str, spacing: int, data_type: str, return_value: Optional[str] = None
    ) -> str:
        description = description.replace("\n", "\n" + ((spacing + 4) * " "))
        if return_value is None:
            # HACK: It's not clear how to use OpenAPI data to identify
            # the `key` fields for objects where e.g. the keys are
            # user/stream IDs being mapped to data associated with
            # those IDs.  We hackily describe those fields by
            # requiring that the descriptions be written as `key_name:
            # key_description` and parsing for that pattern; we need
            # to be careful to skip cases where we'd have `Note: ...`
            # on a later line.
            #
            # More correctly, we should be doing something that looks at the types;
            # print statements and test_api_doc_endpoint is useful for testing.
            arr = description.split(": ", 1)
            if len(arr) == 1 or "\n" in arr[0]:
                return (spacing * " ") + "* " + description
            (key_name, key_description) = arr
            return (
                (spacing * " ")
                + "* "
                + key_name
                + ": "
                + '<span class="api-field-type">'
                + data_type
                + "</span>\n\n"
                + (spacing + 4) * " "
                + key_description
            )
        return (
            (spacing * " ")
            + "* `"
            + return_value
            + "`: "
            + '<span class="api-field-type">'
            + data_type
            + "</span>\n\n"
            + (spacing + 4) * " "
            + description
        )

    def render_table(self, return_values: Dict[str, Any], spacing: int) -> List[str]:
        IGNORE = ["result", "msg", "ignored_parameters_unsupported"]
        ans = []
        for return_value in return_values:
            if return_value in IGNORE:
                continue
            if "oneOf" in return_values[return_value]:
                # For elements using oneOf there are two descriptions. The first description
                # should be at level with the oneOf and should contain the basic non-specific
                # description of the endpoint. Then for each element of oneOf there is a
                # specialized description for that particular case. The description used
                # right below is the main description.
                data_type = generate_data_type(return_values[return_value])
                ans.append(
                    self.render_desc(
                        return_values[return_value]["description"], spacing, data_type, return_value
                    )
                )
                for element in return_values[return_value]["oneOf"]:
                    if "description" not in element:
                        continue
                    # Add the specialized description of the oneOf element.
                    data_type = generate_data_type(element)
                    ans.append(self.render_desc(element["description"], spacing + 4, data_type))
                    # If the oneOf element is an object schema then render the documentation
                    # of its keys.
                    if "properties" in element:
                        ans += self.render_table(element["properties"], spacing + 8)
                continue
            description = return_values[return_value]["description"]
            data_type = generate_data_type(return_values[return_value])
            check_deprecated_consistency(
                return_values[return_value].get("deprecated", False), description
            )
            ans.append(self.render_desc(description, spacing, data_type, return_value))
            if "properties" in return_values[return_value]:
                ans += self.render_table(return_values[return_value]["properties"], spacing + 4)
            if return_values[return_value].get("additionalProperties", False):
                data_type = generate_data_type(return_values[return_value]["additionalProperties"])
                ans.append(
                    self.render_desc(
                        return_values[return_value]["additionalProperties"]["description"],
                        spacing + 4,
                        data_type,
                    )
                )
                if "properties" in return_values[return_value]["additionalProperties"]:
                    ans += self.render_table(
                        return_values[return_value]["additionalProperties"]["properties"],
                        spacing + 8,
                    )
                elif return_values[return_value]["additionalProperties"].get(
                    "additionalProperties", False
                ):
                    data_type = generate_data_type(
                        return_values[return_value]["additionalProperties"]["additionalProperties"]
                    )
                    ans.append(
                        self.render_desc(
                            return_values[return_value]["additionalProperties"][
                                "additionalProperties"
                            ]["description"],
                            spacing + 8,
                            data_type,
                        )
                    )

                    ans += self.render_table(
                        return_values[return_value]["additionalProperties"]["additionalProperties"][
                            "properties"
                        ],
                        spacing + 12,
                    )
            if (
                "items" in return_values[return_value]
                and "properties" in return_values[return_value]["items"]
            ):
                ans += self.render_table(
                    return_values[return_value]["items"]["properties"], spacing + 4
                )
        return ans

    def render_events(self, events_dict: Dict[str, Any]) -> List[str]:
        text: List[str] = []
        # Use argument section design for better visuals
        # Directly using `###` for subheading causes errors so use h3 with made up id.
        argument_template = (
            '<div class="api-argument"><p class="api-argument-name"><h3 id="{h3_id}">'
            "{event_type} {op}</h3></p></div> \n{description}\n\n\n"
        )
        table_link_template = (
            '<div class="events-table-link"><a href="#{url}">{link_name}</a></div>'
        )
        events_table: OrderedDict[str, List[str]] = OrderedDict()
        for events in events_dict["oneOf"]:
            event_type: Dict[str, Any] = events["properties"]["type"]
            event_type_str: str = event_type["enum"][0]
            # Internal hyperlink name
            h3_id: str = event_type_str
            event_name: str = event_type_str
            event_type_str = f'<span class="api-event-name"> {event_type_str}</span>'
            op: Optional[Dict[str, Any]] = events["properties"].pop("op", None)
            op_str: str = ""
            if op is not None:
                op_str = op["enum"][0]
                h3_id += "-" + op_str
                op_type: str = op_str
                op_str = f'<span class="api-event-name">op: {op_str}</span>'
                if event_name in events_table:
                    events_table[event_name] += [op_type]
                else:
                    events_table[event_name] = [op_type]
            else:
                events_table[event_name] = []
            description = events["description"]
            text.append(
                argument_template.format(
                    event_type=event_type_str, op=op_str, description=description, h3_id=h3_id
                )
            )
            text += self.render_table(events["properties"], 0)
            # This part is for adding examples of individual events
            text.append("**Example**")
            text.append("\n```json\n")
            example = json.dumps(events["example"], indent=4, sort_keys=True)
            text.append(example)
            text.append("```\n\n")

        # Creates table of links for events
        events_table_str: List[str] = ['<div class="events-table">']
        sorted_events_table: OrderedDict[str, List[str]] = OrderedDict(sorted(events_table.items()))
        for event_name, ops in sorted_events_table.items():
            if not ops:
                events_table_str.append(
                    table_link_template.format(link_name=event_name, url=event_name)
                )
            else:
                events_table_str.append(f'<div class="events-table-link">{event_name}:</div>')
                events_table_str.append("<div class='events-table-ops'>")
                ops.sort()
                op_list = [
                    table_link_template.format(link_name=f"op: {op}", url=f"{event_name}-{op}")
                    for op in ops
                ]
                events_table_str.extend(op_list)
                events_table_str.append("</div>")
        events_table_str.append("</div>")

        text = events_table_str + text
        return text


def makeExtension(*args: Any, **kwargs: str) -> MarkdownReturnValuesTableGenerator:
    return MarkdownReturnValuesTableGenerator(*args, **kwargs)
