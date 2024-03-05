---
title:
date: 2022-10-24
type: landing 

sections:
 #- block: hero
 #  content:
 #    title: 
 #    image:
 #      # Reference an image in your `assets/media/` folder
 #      filename: logo_colori.png
 #    # Add your Hero text here
 #    text: |
 #      <h6>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut# labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco# laboris nisi ut aliquip ex ea commodo consequat.<h6>
 #      <!doctype html>
 #      <html lang="en">
 #      <body>
 #        <img src="logo.png" align="left" /><p>Your text goes here.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut# labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco# laboris nisi ut aliquip ex ea commodo consequat</p>
 #      </body>
 #      </html>
    

  - block: markdown
    content:
      title: #Quantum Palermo
      subtitle: #Quantum research group of University of Palermo
      text: |
        <html lang="en">
        <body>
          <img src="logo_colori.svg" align="right" hspace="20" vspace="20" width="400" />
          <p>
          Quantum Your text goes here.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut# labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco# laboris nisi ut aliquip ex ea commodo consequat. Your text goes here.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut# labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco# laboris nisi ut aliquip ex ea commodo consequat. 
          </p>
          <img src="logo-colori.svg" align="left" hspace="20" vspace="20" width="400" /> Your text goes here.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut# labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco# laboris nisi ut aliquip ex ea commodo consequat. Your text goes here.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut# labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco# laboris nisi ut aliquip ex ea commodo consequat
        </body>
        </html> 
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
      count: 4
      filters:
        # The folders to display content from
        folders:
          - news
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
      view: masonry
      columns: '2'
      flip_alt_rows: true
  
  - block: markdown
    content:
      text: |
        {{< paige/gallery align="center" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" src="sponsors/mur.webp" >}} 
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" src="sponsors/cnr.png" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" src="sponsors/unipa.png" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" src="sponsors/quantera.jpg" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" src="sponsors/cattedrale3.jpg" >}}
        {{< paige/image class="rounded" style="padding: .2rem" height="6rem" maxheight="5rem" link="https://unipa.it" src="sponsors/cattedrale3.jpg" >}}
        {{< /paige/gallery >}}
        {{< paige/gallery breakpoints=true images="*.jpg" />}}
    design:
      columns: '1'
---