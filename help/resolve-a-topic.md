# Resolve a topic

Zulip's [topics](/help/introduction-to-topics) are very
helpful for customer support, answering questions, investigating
issues and production errors, as well as other workflows.
Resolving topics makes it easy to track the status of each question,
investigation, or notification.

Marking a topic as resolved:

* Puts a ✔ at the beginning of the topic name, e.g., `example topic`
  becomes `✔ example topic`.
* Triggers an automated notice from the [notification
  bot](/help/configure-automated-notices) indicating that you resolved the
  topic. Users can
  [configure](/help/marking-messages-as-read#configure-whether-resolved-topic-notices-are-marked-as-read)
  whether these notices are automatically marked as read.
* Changes whether the topic appears when using the `is:resolved` and
  `-is:resolved` [search filters](/help/search-for-messages#search-filters).

Marking a topic as unresolved removes the ✔ and also triggers an
automated notice from the notification bot.

It's often helpful to define a policy for when to resolve topics that
fits how topics are used in a given channel. Here are some common
approaches for deciding when to mark a topic as resolved:

* **Support**: When the support interaction is complete. Resolving
  topics is particularly useful for internal support teams that might
  not need a dedicated support ticket tracker.
* **Issues, errors and production incidents**: When investigation or
  incident response is complete, and any follow-up work has been
  transferred to the appropriate tracker.
* **Workflow management**: When the work described in the topic is
  complete and any follow-ups have been transcribed.
* **Answering questions**: When the question has been fully answered,
  and follow-ups would be best discussed in a new topic.

Users can resolve or unresolve a topic if they have
[permission](/help/restrict-resolving-topics) to do so.

## Mark a topic as resolved

{start_tabs}

{tab|desktop-web}

{!topic-actions.md!}

1. Select **Mark as resolved**.

!!! tip ""

    You can also click on the **mark as resolved** (<i class="zulip-icon zulip-icon-check"></i>)
    icon in the message recipient bar to mark an unresolved topic as resolved.

{tab|mobile}

{!topic-long-press-menu.md!}

1. Tap **Mark as resolved**.

{!topic-long-press-menu-tip.md!}

{end_tabs}

## Mark a topic as unresolved

Marking a topic as unresolved normally triggers an automated notice from the
notification bot. However, unresolving a topic right after you resolved it
removes the original notice instead. This is helpful if you resolved a topic by
accident.

{start_tabs}

{tab|desktop-web}

{!topic-actions.md!}

1. Select **Mark as unresolved**.

!!! tip ""

    You can also click on the **ellipsis** (<i class="zulip-icon zulip-icon-more-vertical"></i>)
    in the message recipient bar, and select the **Mark as unresolved** option.

{tab|mobile}

{!topic-long-press-menu.md!}

1. Tap **Mark as unresolved**.

{!topic-long-press-menu-tip.md!}

{end_tabs}

## Search for messages in unresolved topics

{start_tabs}

{tab|desktop-web}

1. Click the **search** (<i class="search_icon zulip-icon
   zulip-icon-search"></i>) icon in the top bar to open the search box.

1. Type `-is:resolved`, or start typing and select **Exclude topics marked as
   resolved** from the typeahead.

1. _(optional)_ Enter additional search terms or
   [filters](/help/search-for-messages).

1. Press <kbd>Enter</kbd>.

!!! keyboard_tip ""

    You can also use the <kbd>/</kbd> or <kbd>Ctrl</kbd> + <kbd>K</kbd>
    keyboard shortcut to start searching messages.

{end_tabs}

!!! tip ""

    To get a feed of unread messages in all unresolved topics, search for
    `is:unresolved is:unread`.

## Search for messages in resolved topics

{start_tabs}

{tab|desktop-web}

1. Click the **search** (<i class="search_icon zulip-icon
   zulip-icon-search"></i>) icon in the top bar to open the search box.

1. Type `is:resolved`, or start typing and select **Topics marked as resolved**
   from the typeahead.

1. _(optional)_ Enter additional search terms or
   [filters](/help/search-for-messages).

1. Press <kbd>Enter</kbd>.

!!! keyboard_tip ""

    You can also use the <kbd>/</kbd> or <kbd>Ctrl</kbd> + <kbd>K</kbd>
    keyboard shortcut to start searching messages.

{end_tabs}

## Filter by whether topics are resolved

{!filter-resolved-left-sidebar.md!}

## Configure whether resolved topic notices are marked as read

{!configure-resolved-notices-marked-as-read.md!}

## Sending messages to resolved topics

You can send messages to a resolved topic, which is handy for _"thank you"_
messages, or to discuss whether a topic was incorrectly marked as resolved.

When a topic is resolved or unresolved, users' compose boxes and message views
automatically update to show the topic's current state. This helps make sure
everyone sends messages to the correct place.

[Integrations](/help/integrations-overview) will still send messages to the
original topic after a topic is resolved. This is useful for alerting
integrations, where a repeating alert might have a different cause. As usual,
you can mark the topic resolved once you've investigated the situation.

## Related articles

* [Rename a topic](/help/rename-a-topic)
* [Move content to another topic](/help/move-content-to-another-topic)
* [Restrict topic editing](/help/restrict-moving-messages)
* [API documentation for resolving topics](/api/update-message)
