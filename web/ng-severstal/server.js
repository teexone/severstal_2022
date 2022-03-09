const express = require('express')

app = express()
app.use('/', express.static('dist/ng-severstal'))

app.listen(80, () => {
  console.log("Server is running")
})
