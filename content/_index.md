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
        flip_alt_rows: true
      show_interests: false

  - block: portfolio
    content:
      title: Upcoming Events
      subtitle: 
      text: 
      count: 2
      filters:
        # The folders to display content from
        folders:
          - events
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
      background:
        color: "rgb(247, 247, 247)"
      view: showcase
      columns: '2'
      flip_alt_rows: false
      
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
      background:
        color: "rgb(255,255,255)"
      columns: '2'
      view: masonry
      flip_alt_rows: true

  - block: collection
    content:
      title: Latest News
      subtitle: Papers, Projetcs and ...
      text: 
      count: 4
      filters:
        # The folders to display content from
        folders:
          - publication
          #- news
          - seminars
          #- events
          - projects
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
      background:
        color: "rgb(247, 247, 247)"
      view: card
      columns: '2'
      flip_alt_rows: true
  
  - block: markdown
    content:
      text: |
        {{< paige/gallery align="center" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" 
        src="./sponsors/unipa.jpeg" >}} 
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://prin.mur.gov.it/" 
        src="./sponsors/prin.jpeg" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://marie-sklodowska-curie-actions.ec.europa.eu/" 
        src="./sponsors/marie-curie.jpg" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://qucom.eu/" 
        src="./sponsors/corsimo.jpg" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://gow.epsrc.ukri.org/NGBOViewGrant.aspx?GrantRef=EP/T028106/1" 
        src="./sponsors/epsrc.jpg" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://royalsociety.org/" 
        src="./sponsors/royal.png" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="" 
        src="./sponsors/ibm.png" >}}
        {{< /paige/gallery >}}
        {{< paige/gallery breakpoints=true images="*.jpg" />}}
        <p class="text-center">
        <a class="lead" href="../../research_lines/">Back</a></p>
    design:
      background:
        color: "rgb(255,255,255)"
      columns: '1'
---

