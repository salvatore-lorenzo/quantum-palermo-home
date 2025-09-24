---
title:
date: 2022-10-24
type: landing

sections:
  - block: collection
    id: events
    content:
      title: Past Events
      subtitle: "[Back](../../news)"
      text: 
      filters:
        folders:
          - events
        tags: [event]
        exclude_tags: [pastevents]
        kinds:
          - event
      sort_by: 'Date'
      sort_ascending: false
      default_button_index: 0
    design:
      columns: '2'
      # Choose a listing view
      view: showcase
      # For Showcase view, flip alternate rows?
      flip_alt_rows: true
---
