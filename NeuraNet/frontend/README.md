#Intro

This is the frontend to the Banbury Cloud Desktop Applicaiton. The primary reason why I chose to implement this through
electron is because I needed the ability to perform operations on the device. This is difficult to do in a web app.  


## Major technologies

- [React.js 18](https://reactjs.org/)
- [Electron 19](https://www.electronjs.org/)
- [MUI 5](https://mui.com/) (formerly Material-UI)
- [Webpack 5](https://webpack.js.org/)
- Typescript, ESLint, and Prettier are used to improve the developer experience

## Requires
- [Node.js 16.x](https://nodejs.org/en/)
- [NPM >= 7.x](https://github.com/npm/cli)

## Getting Started

1. Using NPM 7+, run the following command to install dependencies

```sh
npm install
```

2. Run the following command to build and start the development version of your app with live reloading.

```sh
npm run dev
```

## Packaging

Run `npm run package` to build and package your electron app.

Run `npm run deploy` to build and package your electron app, along with creating the necessary installers.

## Common issues

### xcrun: error: invalid active developer path

This is caused when elecron-builder tries to sign a build. Run `xcode-select --install` to install the necessary Xcode tools.


## Contributing

Pull requests are always welcome 😃.

## License

This project is licensed under the terms of the [MIT license](LICENSE).
