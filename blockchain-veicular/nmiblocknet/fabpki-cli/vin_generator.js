function makeVin() {
    var vinGenerator = require('vin-generator');
    var randomVIn = vinGenerator.generateVin();
    return randomVIn
}
console.log(makeVin())
