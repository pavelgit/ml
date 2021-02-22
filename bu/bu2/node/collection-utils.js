const getOneHotEncoding = (data, objectGetter)  => {
    const valueArrays = data.map(v => Object.keys(objectGetter(v)));
    const values = [].concat.apply([], valueArrays);
    const distinctValues = [...new Set(values)];
    const encoding = {};
    distinctValues.forEach((v, i) => {
        encoding[v] = i;
    });
    return encoding;
};

const toDictionary = (values, keySelector, valueSelector) => {
    const dict = {};
    for (const v of values) {
        dict[keySelector(v)] = valueSelector(v);
    }
    return dict;
};

const objectToOneHot = (object, encoding) => {
    
    const result = new Array(Object.values(encoding).length);
    result.fill(0);
    for (const key of Object.keys(object)) {
        result[encoding[key]] = object[key];
    }
    return result;
    
};

const buildPayload = (data, rawGetters, oneHotGetters) => {

    const rawFields = Object.keys(rawGetters);
    const oneHotFields = Object.keys(oneHotGetters);

    const oneHotEncodings = toDictionary(oneHotFields, field => field, field => getOneHotEncoding(data, oneHotGetters[field]));

    const payload = [];

    for (const v of data) {
        const array = [];
        for (const field of rawFields) {
            array.push(rawGetters[field](v));
        }            
        for (const field of oneHotFields) {
            array.push(...objectToOneHot(oneHotGetters[field](v), oneHotEncodings[field]));
        }  
        payload.push(array);
    }
    return { oneHotEncodings, payload };
};

module.exports = {
    toDictionary,
    buildPayload
};