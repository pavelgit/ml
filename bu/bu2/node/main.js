const moment = require('moment');
const fs = require('promise-fs');

const JSONStream = require('JSONStream');
const es = require('event-stream');
const jsonUtils = require('./json-utils.js');
const collectionUtils = require('./collection-utils');
const { GROUP2 } = require('./groups'); 

const getAge = bd => moment().diff(moment(bd), 'years');

const rawInputGetters = {
    age: v => getAge(v.calculationInput.birthday),
    staffResponsibility: v => Number(v.calculationInput.staffResponsibility),
    benefitAmount: v => Number(v.calculationInput.benefitAmount),
    fractionOfficeWork: v => Number(v.calculationInput.fractionOfficeWork),
    smoker: v => Number(v.calculationInput.smoker),
    benefitAgeLimit: v => Number(v.calculationInput.benefitAgeLimit),
    adjustment: v => Number(Boolean(v.calculationInput.adjustment))
};

const oneHotInputGetters = {
    //occupation: v => ({ [v.calculationInput.occupation]: 1 }),
    excellentPerformance: v => ({ [v.calculationInput.excellentPerformance]: 1 }),
    educationType: v => ({ [v.calculationInput.educationType]: 1 }),
    jobSituation: v => ({ [v.calculationInput.jobSituation]: 1 }),
    industry: v => ({ [v.calculationInput.industry]: 1 }),
    dynamicPremium: v => ({ [v.calculationInput.dynamicPremium]: 1 }),
    familyStatus: v => ({ [v.calculationInput.familyStatus]: 1 })
};

const oneHotOutputGetters = {
    /*exists: v => collectionUtils.toDictionary(
        v.prices, 
        p => `${p.insuranceName} -> ${p.tariffName}`, 
        p => 1             
    ),*/
    nettoPrice: v => collectionUtils.toDictionary(
        v.prices, 
        p => `${p.insuranceName} -> ${p.tariffName}`, 
        p => Number(p.nettoPrice)
    ),
    /*bruttoPrice: v => collectionUtils.toDictionary(
        v.prices, 
        p => `${p.insuranceName} -> ${p.tariffName}`, 
        p => Number(p.bruttoPrice)
    )*/
};

const main = async () => {

    const data = (await jsonUtils.loadJson('./../data/data.json', 46000))
        .filter(v => GROUP2.includes(v.calculationInput.occupation));

    data.forEach(v => { v.prices = v.prices.filter(
        price => price.insuranceName === 'DEVK' && price.tariffName === 'N BU'
    ); });

    console.log('data.length', data.length);

    const { oneHotEncodings: oneHotInputEncodings, payload: input } = 
        collectionUtils.buildPayload(data, rawInputGetters, oneHotInputGetters);

    const { oneHotEncodings: onwHotOutputEncodings, payload: output } = 
        collectionUtils.buildPayload(data, {}, oneHotOutputGetters); 

    await jsonUtils.saveSmallJson('./../data/input-encodings.json', oneHotInputEncodings);
    await jsonUtils.saveJsonArray('./../data/input.json', input);
    
    await jsonUtils.saveSmallJson('./../data/output-encodings.json', onwHotOutputEncodings);
    await jsonUtils.saveJsonArray('./../data/output.json', output);

    console.log('finished!');
}

main();
/*
"birthday": "1988-12-22",
"staffResponsibility": "0",
"benefitAmount": "1400",
"useFBTipper": false,
"occupation": "Bürokaufmann,frau",
"excellentPerformance": false,
"debug": false,
"educationType": "Berufsausbildung",
"jobSituation": "Angestellt/Selbstständig",
"fractionOfficeWork": "80",
"industry": "Sonstige Branche",
"insuranceStart": "2018-03-01",
"dynamicPremium": "dynamic_premium_3_percent",
"smoker": false,
"benefitAgeLimit": "65",
"adjustment": false,
"salutation": "Herr",
"ignorePriceCache": false,
"familyStatus": "Keine Angabe"
*/