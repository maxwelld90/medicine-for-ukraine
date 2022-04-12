module.exports = {
  proseWrap: 'never',
  printWidth: 110,
  tabWidth: 2,
  singleQuote: true,
  semi: false,
  trailingComma: 'es5',
  arrowParens: 'always',
  overrides: [
    {
      files: '*.{js,jsx,tsx,ts,scss,json,html}',
      options: {
        tabWidth: 2,
      },
    },
  ],
}
