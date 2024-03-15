---
title:
date: 2022-10-24
type: landing 



sections:
  - block: myabout
    content:
      username: 'admin'
      text:
      design:
        columns: '2'
      show_interests: false
      
  - block: portfolio
    id: research
    content:
      title: Research Lines
      subtitle: Our research focuses on
      text: 
      filters:
        folders:
          - research_lines
        tags: []
        exclude_tags: []
        kinds:
          - page
      sort_by: 'tags'
      sort_ascending: false
      default_button_index: 0
    design:
      columns: '2'
      view: masonry
      flip_alt_rows: true

  - block: collection
    content:
      title: Latest News
      subtitle: Seminars, Papers and ...
      text: 
      count: 4
      filters:
        # The folders to display content from
        folders:
          - news
          - seminars
          - events
          #- projects
          - publication
        author: ""
        category: ""
        tag: ""
        publication_type: ""
        featured_only: false
        exclude_featured: false
        exclude_future: false
        exclude_past: false
      offset: 0
      order: desc
      page_type: 
    design:
      view: card
      columns: '2'
      flip_alt_rows: true
  
  - block: markdown
    content:
      text: |
        {{< paige/gallery align="center" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" 
        src="./sponsors/unipa.jpeg" >}} 
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" 
        src="./sponsors/prin.jpeg" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" 
        src="./sponsors/ibm.png" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" 
        src="./sponsors/corsimo.jpg" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" 
        src="./sponsors/epsrc.jpg" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" 
        src="./sponsors/royal.png" >}}
        {{< /paige/gallery >}}
        {{< paige/gallery breakpoints=true images="*.jpg" />}}
        <p class="text-center">
        <a class="lead" href="../../research_lines/">Back</a></p>
    design:
      columns: '1'
---
