# Question and Answer Community (a template for yppm)

## Warning 
Do not use npm or related online tools. Otherwise you can't built your software 20 years later.

Use pure text as much as possible, like pure python text or old php text. But here the text is just a bytes list, who knows what it could be 50 years later. The text encoding changes.

So this is a bad example.

## Todo
For this website, it should be as simple as possible

For example, it should have a home page, the home page is a search list. In home page, it should have a chat button where when user click that button, a chat page will pop up. For the chat page, 80% of the top page is the message list view, the bottom is an input box.

When user do a search, we'll show title list with detail link, and before those links, it should have previous_page, next_page buttons.

This website should also have another page, which is the detail page, where it has title, description, answers, comments.

If a user want to create/edit/check a question/answer/comment, they will do it at detail page.

**I have to make sure there have one public account for everyone to add stuff. So they don't have to register/login to add question and comment** (In the end, I simply cut off the whole user system)

**In the end, it should look like 知*乎+T*tter(no char limitation)**

> For `robots.txt`, it will use pages generated by "python + pure html + pure css code", which is different than those page I descriped above, for example, in `/pure/*.html`, the `*` is the post id.

> You can even do it in a more extrem way, for example, generate those pages by "python + rendered png image + pure markdown text"(html title is question title, html description is question description, picture is in html base64 format, escaped markdown string is in html comment after json.dumps(*) at the bottom), put those html page in `/extream_pure/*.html`, the `*` is the post id.

> If I have to give a defination for the UI design of this project, that would be "people_as_service".
