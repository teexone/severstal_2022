const express = require('express')
const path = require('path')

app = express()
app.use(express.static(path.join(__dirname, 'dist/ng-severstal')))

app.get('/*', async (req, res) => {
    res.sendFile(path.resolve(__dirname, 'dist/ng-severstal', 'index.html'));
});

app.listen(80, () => {
  console.log("Server is running")
})

