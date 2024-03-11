---
title: People
date: 

type: landing

sections:
  - block: mypeople
    content:
      title: 
      # Choose which groups/teams of users to display.
      #   Edit `user_groups` in each user's profile to add them to one or more of these groups.
      user_groups:
          - Staff
          - Postdoctoral Researchers
          - PhD Students
          - Visiting & Friends
      sort_by: Params.last_name
      sort_ascending: true
    design:
      show_interests: false
      show_role: true
      show_social: true
      columns: '2'
  - block: markdown
    id: button
    content:
      title: 
      subtitle: 
      text: |
        <p class="text-center">
        <a class="lead" href="../../">Back</a></p>
    design:
      columns: 2
---