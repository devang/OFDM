#!/usr/bin/env node
'use strict';

// WiMax-like profiles
// 802.16d
const p0 = {
    fftLen: 256, // 2^8
    nDatBins: 2 * 8 * 12, // 192
    nPilots: 8,
    pilotOffset: 13,
    pilotStep: 24,
    dcGap: 1
};

// 802.16e
const p1 = {
    fftLen: 128,
    nDatBins: 12 * 6, // 72
    nPilots: 12,
    pilotOffset: 4,
    pilotStep: 6,
    dcGap: 1,
};

const p2 = {
    fftLen: 256,
    nDatBins: 12 * 8, // 96
    nPilots: 96,
    pilotOffset: 0,
    pilotStep: 2,
    dcGap: 1,
};

const p = p2;

const nGuardBand = p.fftLen - p.dcGap - p.nDatBins - p.nPilots; // 55

console.log(nGuardBand);

const res = {
    dat: [],
    pil: []
};

let count = p.nDatBins / 2;
for (let i = (p.dcGap + 1) / 2, ilen = (p.fftLen / 2); i < ilen; i++) {
    if(((i - p.pilotOffset) % p.pilotStep) === 0) {
        res.pil.push(i);
        res.pil.push(-i);
    } else {
        res.dat.push(i);
        res.dat.push(-i);
        count -= 1;
    }
    if (count === 0) {
        break;
    }
}

console.log(`(${res.dat.join(', ')})\n(${res.pil.join(', ')})`);
