---
title:
date: 2022-10-24
type: landing 

sections:
  - block: markdown
    content:
      title: Quantum Palermo
      subtitle: Quantum research group of University of Palermo
      text: |
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
        
        {{% paige/image class="rounded-lg" src="cattedrale2.jpg" height=20rem width="100%" %}}
        <br>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum
  
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
      sort_by: 'Title'
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
      count: 5
      offset: 0
      order: desc
      page_type:  news 
    design:
      view: list
      columns: '2'
  
  - block: markdown
    content:
      text: |
        {{< paige/gallery align="center" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" src="sponsors/cattedrale3.jpg" >}} 
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" src="sponsors/cattedrale3.jpg" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" src="sponsors/cattedrale3.jpg" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" src="sponsors/cattedrale3.jpg" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" src="sponsors/cattedrale3.jpg" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" src="sponsors/cattedrale3.jpg" >}}
        {{< /paige/gallery >}}
        {{< paige/gallery breakpoints=true images="*.jpg" />}}
    design:
      columns: '1'
---

ciao 