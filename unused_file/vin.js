
const vindec = require('vindec');
var vinGenerator = require('vin-generator');

var randomVin = vinGenerator.generateVin();
//
//console.log(`${vindec.validate('JM1BK32GX97ELPTE0')}`)
console.log(JSON.stringify(vindec.decode('ZFFEW58A660144998'))) 