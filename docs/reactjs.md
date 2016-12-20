Help
====

**If You want to develop with reactjs, please install nodejs packages**

```sh
$ make npm-install
```

**Then in dev mode, you can run watch mode with js modification**

```sh
$ make watch-mode
```

**Finally If you want to publish the js**

```sh
$ make build-prod-js
```

Code Tree
---------

index.js is the webpack entrypoint, (about/hosts/overview/system\_status/release\_history) is the panel view, top\_nav.js is the Top Nav view, left\_nav.js is the Left nav bar view.

If want to develop react js, you can run watch-mode, then modify the js code in react directory.

- __react__
  - [DevTools.js](src/static/js/react/DevTools.js)
  - __about__ [](Comment text goes here)
  - __actions__
    - [index.js](src/static/js/react/actions/index.js)
    - [notification.js](src/static/js/react/actions/notification.js)
  - __chains__
  - __helpers__
    - [Paginator.jsx](src/static/js/react/helpers/Paginator.jsx)
    - [index.js](src/static/js/react/helpers/index.js)
    - [paginate.js](src/static/js/react/helpers/paginate.js)
  - __hosts__
  - [index.js](src/static/js/react/index.js)
  - [left_nav.js](src/static/js/react/left_nav.js)
  - __overview__
  - __reducers__
    - [index.js](src/static/js/react/reducers/index.js)
  - __release_history__
  - [routes.js](src/static/js/react/routes.js)
  - __style__
    - [table.css](src/static/js/react/style/table.css)
  - __system_status__
    - [view.js](src/static/js/react/system_status/view.js)
  - [top_nav.js](src/static/js/react/top_nav.js)