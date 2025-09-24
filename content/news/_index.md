---
title:
date: 2022-10-24
type: landing

sections:
  - block: Portfolio
    content:
      title: Upcoming Events
      subtitle: |
        <p class="text-center">
        <a class="lead" href="../../">Back</a></p> 
      text: 
      count: 3
      filters:
        # The folders to display content from
        folders:
          - news
        tags: []
        exclude_tags: [past]
      offset: 0
      sort_by: 'date'
      sort_ascending: false
    design:
      view: showcase
      columns: '2'
      flip_alt_rows: True

  - block: markdown
    id: button
    content:
      title: 
      subtitle: #"[Events](../events) & [Seminars](../seminars)"
      text: |
        <style unselectable="on">
        /* Ensure the iframe adjusts properly on small screens */
        iframe {
        width: 100%;  /* Adjust to full width */
        max-width: 1200px;
        height: 500px;
        border: none;
        }
        </style>
        <div id="wrap" unselectable="on">
            <iframe id="open-web-calendar" 
                style="background:url('https://raw.githubusercontent.com/niccokunzmann/open-web-calendar/master/static/img/loaders/circular-loader.gif') center center no-repeat;"
                src="https://open-web-calendar.hosted.quelltext.eu/calendar.html?url=https://outlook.office365.com/owa/calendar/6e7129fbb9d84cef85adbc5afa79637e@unipa.it/a7e1ae6bdd9444efb29ff20838071e1411365429934934175301/calendar.ics"
                sandbox="allow-scripts allow-same-origin allow-top-navigation"
                allowTransparency="true" scrolling="yes" 
                frameborder="0." height="500px" width="100%"></iframe>
        </div>        
    design:
      columns: 1 
  
  - block: Portfolio
    content:
      title: Past Events
      subtitle: |
        <p class="text-center">
        <a class="lead" href="../../">Back</a></p> 
      text: 
      count: 2
      filters:
        # The folders to display content from
        folders:
          - news
        tags: []
        exclude_tags: [future]
      offset: 0
      sort_by: 'date'
      sort_ascending: false
      page_type: 
    design:
      view: showcase
      columns: '2'
      flip_alt_rows: true
  #- block: collection
  #  id: news
  #  content:
  #    title: News
  #    subtitle: "[Events](../events) & [Seminars](../seminars)"
  #    text: 
  #    filters:
  #      # Folders to display content from
  #      folders:
  #        - events
  #        - seminars
  #      # Only show content with these tags
  #      tags: []
  #      # Exclude content with these tags
  #      exclude_tags: []
  #      # Which Hugo page kinds to show (https://gohugo.io/templates/section-templates/##page-kinds)
  #      kinds:
  #        - page
  #    # Field to sort by, such as Date or Title
  #    sort_by: 'Date'
  #    sort_ascending: false
  #    # Default portfolio filter button
  #    # 0 corresponds to the first button below and so on
  #    # For example, 0 will default to showing all content as the first button below shows #content with *any* tag
  #    default_button_index: 0
  #    # Filter button toolbar (optional).
  #    # Add or remove as many buttons as you like.
  #    # To show all content, set `tag` to "*".
  #    # To filter by a specific tag, set `tag` to an existing tag name.
  #    # To remove the button toolbar, delete the entire `buttons` block.
  #    #buttons:
  #    #  - name: All
  #    #    tag: '*'
  #    #  - name: OQS 
  #    #    tag: OQS
  #    #  - name: QT
  #    #    tag: QT
  #  design:
  #    # See Page Builder docs for all section customization options.
  #    # Choose how many columns the section has. Valid values: '1' or '2'.
  #    columns: '2'
  #    # Choose a listing view
  #    view: list
  #    # For Showcase view, flip alternate rows?
  #    flip_alt_rows: true
  #- block: markdown
  #  id: button
  #  content:
  #    title: 
  #    subtitle: 
  #    text: |
  #      <p class="text-center">
  #      <a class="lead" href="../../">Back</a></p>
  #  design:
  #    columns: 2  1
---