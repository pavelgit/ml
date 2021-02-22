const JSONStream = require('JSONStream');
const es = require('event-stream');
const fs = require('promise-fs');

const loadJson = async (fileName, limit = -1) => {
    const getStream = function () {
        const stream = fs.createReadStream(fileName, {encoding: 'utf8'}),
            parser = JSONStream.parse('*');
            return stream.pipe(parser);
    };

    return new Promise(resolve => {
        let resolved = false;
        const data = [];
        getStream()
        .pipe(es.mapSync(function (v) {
            data.push(v);
            if (data.length % 100 === 0 && !resolved) {
                console.log('read: ', data.length);
            }
            if (data.length===limit) {
                resolved = true;
                resolve(data);
            }
        }))
        .on('close', () => {
            if (!resolved) {
                resolve(data);
            }
        });
    });
}

const saveJsonArray = (fileName, array) => {
    return new Promise(resolve => {
        var transformStream = JSONStream.stringify();
        var outputStream = fs.createWriteStream(fileName );
        
        // In this case, we're going to pipe the serialized objects to a data file.
        transformStream.pipe( outputStream );
        
        // Iterate over the records and write EACH ONE to the TRANSFORM stream individually.
        // --
        // NOTE: If we had tried to write the entire record-set in one operation, the output
        // would be malformed - it expects to be given items, not collections.
        array.forEach( transformStream.write );
        
        // Once we've written each record in the record-set, we have to end the stream so that
        // the TRANSFORM stream knows to output the end of the array it is generating.
        transformStream.end();
        
        // Once the JSONStream has flushed all data to the output stream, let's indicate done.
        outputStream.on(
            "finish",
            function handleFinish() {
    
                resolve();
            }
        );
    });
};

const saveSmallJson = (fileName, o) => fs.writeFile(fileName, JSON.stringify(o, null, 4));

module.exports = {
    loadJson, 
    saveJsonArray,
    saveSmallJson
};