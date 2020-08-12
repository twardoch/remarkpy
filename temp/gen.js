var avro = require('avsc');

function make_schema(obj){
    return avro.Type.forValue(obj);
}

exports.make_schema = make_schema;
