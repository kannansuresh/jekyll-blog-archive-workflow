## Jekyll Archives Workflow

This workflow action helps in creating Jekyll archives for GitHub pages.

## Steps to follow

### 1. On your Jekyll Blog

1. Open `_config.yml` file to edit your configuration.
2. Add a collection to the configuration like below.
   
```yml
# Archives
collections:
  archives:
    output: true
    permalink: /archives/:path/
```

3. Create a folder `_archives` in your GitHub pages root.
4. Create a text file `archivedata.txt` with the below code.

<!-- {% raw %} -->

```liquid
---
---
{
"categories": [
    {%- for category in site.categories -%}
    "{{ category[0]}}"{% unless forloop.last %},{% endunless %}
    {%- endfor -%}
],
"tags": [
    {%- for tag in site.tags -%}
    "{{ tag[0] }}"{% unless forloop.last %},{% endunless %}
    {%- endfor -%}
],
"years": [
    {%- for post in site.posts -%}
    "{{ post.date | date: "%Y" }}"{% unless forloop.last %},{% endunless %}
    {%- endfor -%}
]
}
```
<!-- {% endraw %} -->

![Archive setup](/assets/images/archive-files-setup.jpg)

1. Build your site and see if you can see the archive data by navigating to your site. `(yoursite.com/archives/archivedata)`
   
2. You should see a `json` file like the below one. 
```json
{
    "categories": [
        "Software Testing",
        "Excel",
        "Blogging",
        "Programming",
        "Quiz",
        "Photography",
        "RPA"
    ],
    "tags": [
        "Automation Testing",
        "UFT",
        "QTP",
        "Excel VBA"
    ],
    "years": [
        "2020",
        "2020",
        "2019",
        "2018",
        "2017"
    ]
}
```

> File was formatted for better reading. This will appear minified on your site.

7. Create 3 layouts in the `_layouts` folder.
    - `archive-categories.html`
    - `archive-tags.html`
    - `archive-years.html`

> Sample layouts and files are present in the folder `blog-files` of this repository. If you are using it make sure to include a file from `_includes` folder too.

## 2. Setup a new action

1. Got to your blog repository.
2. Create a folder named `.github` and create `workflows` folder inside it if it doesn't exist.
3. Create a new file named `add_archives.yml` in the `workflows` folder. You can name it anything you want.
4. Add the following code inside the file.
   
```yml
name: Generate Jekyll Archives
# description: Generate categories, tags and years archive files.
on:
  workflow_dispatch:
  push:
    paths:
      - "_posts/**"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Generate Jekyll Archives
        uses: kannansuresh/jekyll-blog-archive-workflow@master
        with:
          archive_url: "https://aneejian.com/archives/archivedata"
          archive_folder_path: "_archives"

      - name: setup git config
        run: |
          git config user.name "GitHub Actions Bot"
          git config user.email "<>"

      - name: commit
        run: |
          git add --all
          git commit -m "Created and updated archive files." || echo "No changes to commit."
          git push origin master || echo "No changes to push."
```

### Variables

| Variable Name | Description |Required |
|--|--|--|
| `archive_url` | Your blog's archive data URL. e.g. `yoursite.com/archives/archivedata` | Yes |
|`archive_folder_path`|Path to your `_archives` folder. Default value `_archives`|Yes|

> In the code above, make sure to change the variable `archive_url` to your site's archive data URL.

> By default, the code pushes changes to `master` branch. Change the code if you want the changes to be pushed to a different branch.

> The action is set to run every time a commit happens in your `_posts` folder.


![Archive files created by action](/assets/images/archive-files-created-with-action.jpg)

1. To trigger the action manually
   - Navigate to `Actions` tab.
   - Select `Generate Jekyll Archives`.
   - Select `Run workflow` and run it.
   - Wait for the run to complete.
   - After a successful run, navigate to `_archives` folder and you will see the archive files generated.


To view the archives on your site, use the following URLs.
- For categories: `yoursite.com/category/category_name`
- For tags: `yoursite.com/tag/tag_name`
- For categories: `yoursite.com/year/2020`

## See it in action
I have implemented this on my website [Aneejian](https://aneejian.com)

See the below URLs.
- [https://aneejian.com/category/rpa](https://aneejian.com/category/rpa)
- [https://aneejian.com/tag/jekyll](https://aneejian.com/tag/jekyll)
- [https://aneejian.com/year/2020](https://aneejian.com/year/2020)