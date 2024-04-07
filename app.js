var express = require('express');
var path = require('path');
const { spawn } = require('child_process')

const app = express();
const port = 3000;

//options
app.set('view engine', 'pug');
app.set('views', path.join(__dirname, '/public/views'));

app.use(express.static(__dirname + '/public'));

app.get('/', (req, res) => {
    res.render('index');
});

app.get('/searchpage', (req, res) => {
    console.log("RECEIVED searchpage")
    var key = req.query.keyword.toLowerCase();
    res.render('search', {keyword: key});
});

app.get('/search', (req, res) => {
    console.log("RECEIVED")
    var keyword = req.query.keyword.toLowerCase();

    if (keyword == "test")
    {
        //Render Test Website
        res.status(200).json({"mean": 100000, "gradient": 0.1, "peak": "2024-01-05 04:00:00", "minimum": 38088, "maximum": 4810298,
        "intercept": 73, "currentInterest": 68, "image_link": `graphs/google.png`});
    }
    else
    {
        const childPython = spawn('python', ['engine.py', keyword]);

        var sent = 0;

        childPython.stdout.on('data', (data) => {
            console.log(data.toString());
            console.log(JSON.parse(data.toString()));
            output = JSON.parse(data.toString());
            res.status(200).json({"mean": output.mean, "gradient": "-", "peak": output.peak, "minimum": output.minimum, "maximum": output.maximum,
                                  "intercept": "-", "currentInterest": "-","image_link": `graphs/${keyword}.png`});
            sent = 1;
        });

        var stderrChunks = [];

        childPython.stderr.on('data', (data) => {
            console.log(data);
            stderrChunks = stderrChunks.concat(data);
        });

        childPython.stderr.on('end', () => {
            console.log(Buffer.concat(stderrChunks).toString());
            if (!sent){
                res.status(429).json({"error": "Too many requests, try again!"});
            }
        });
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`)
});