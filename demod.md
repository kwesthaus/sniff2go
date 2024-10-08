inspectrum is weird, it's AM from the reader as verified by constellation plot in grc
center 287k, bandwidth 800k works

there are definitely 2 different "pulses" of carrier tone by reader that are repeated forever as a pair
- carrier drops between pulses and pairs of pulses
(SEGO)
first pulse is longer overall, has 2 modulated sections - 1 short, 1 long
- can't id first cmd - seems like 8 0-bits, 2 calibrations, a confusing 0-bit, then 17 more normal bits
- second cmd - again with the 8 0-bits, 2 calibrations, a confusing 0-bit, but now 89 more normal bits
(6C)
second one is shorter overall, has 2 modulated sections - 2 short
- both query (preamble + 22 bits)







6C DECODING
- RTcal in query command is ~19us, logic-0 is then ~6us, that checks out for 106.67kbps
- TRcal in query command is ~33us, (64/3) / (33 / 1_000_000) = 640khz Backscatter Link Frequency
    - 64/3 comes from decoded query command
    - m = 2 in the decoded query command, so data rate is 640/2 = 320kbps, which is the max speed listed for subcarrier modulation
- reader: 2ASK, PIE (logic 0: 10, logic 1: 1110), 106.67kbps (average) data (160kbps for logic 0, 80kbps for logic 1)
- tag: ? modulation, 2 Miller subcarrier (2 cycles per bit period, transition between double 0s and in middle of 1)

preamble followed by:
(length) 4444 1 22 1 22 22 1 4444 55555
(value)  1000 1 01 1 00 00 0 0000 01101
(value)  1000 1 01 1 00 00 1 0000 10000

cmd=query, dr=64/3, m=2, pilot_tone=yes, select=all, target=A, Q=0, CRC=13
cmd=query, dr=64/3, m=2, pilot_tone=yes, select=all, target=B, Q=0, CRC=16

queries are 22 bits
first one has 7 one-bits, other has 6
6 
(6 * 2) + (16 * 1) = 28 * 6.25(us per logic-0) = 175us
.610 
.785
=
.175
based on timing, 0-bit is 6.25us and a 1-bit is 2xtime period of 0-bit
1000000 / (1.5 * 6.25) = 106.667kbps

TAG:
- from query, m = 2 (miller subcarrier) and divide ratio = 3/64






SEGO DECODING
- reader: 2ASK, manchester, 80kbps data (160kbps manchester)

for the other pulse group:

0.9315
1.4000
0.4685
28 bits, 9 ones
(9 * 2) + 19 = 37

.4685 / 37 = 0.0125
period is 12.5us for the data in the first "pulse" that I can't figure out, that's 80kbd

ohhhhhhhh it's probably scanning for ISO 18000-6 type B (ISO 18000-62) tags as well (as opposed to 18000-6 type C aka 18000-63)
yup one of the options for reader modulation/encoding/speed for 6 type B is 40kbps manchester ASK

so ISO 18000-63 is same as EPC Class 1 Gen 2, is there an equivalent for 18000-62 so I can read the EPC spec to get the command values?

also from google maps the readers are now transcore, NOT sirit
https://www.google.com/maps/@47.6370355,-122.2357994,3a,15y,275.38h,127.54t/data=!3m6!1e1!3m4!1sKgVStuBWTP8lf52TLmFMTw!2e0!7i16384!8i8192

ahhhhh from doing some more reading about WSDOT/Transcore, found the map here:
https://wsdot.wa.gov/sites/default/files/2021-10/Annual-Report-2019.pdf
Transcore has their own proprietary protocol based on ISO 18000-62 called Super eGo ("SeGo")

ahhhh would you look at that, they published their spec in the name of interoperability! sounds familiar
https://transcore.com/transcore-facilitates-nationwide-toll-interoperability.html
https://transcore.com/sego-specs

transcore stuff definitely supports different tag formats
https://transcore.com/wp-content/uploads/2022/01/16-0088-001-Rev-C-E4-Wiegand-Translator.pdf


preamble (18 non-manchester bits): 9x01 (0x5555 then another 0b01)
check (10 non-manchester bits): 1100111010 (0xce then another 0b01)
combined, preamble and check are 0x5555 73a
data (manchester)
crc (manchester): 16 bits

first command:
01010101 10011001 10011010 10101010 01100101 01100110 (before manchester decode)
0x55 99 9a aa 65 66 before manchester decode
00001010 1011111101000101 (after manchester decode)
0x0abf45 after manchester decode

initialize, crc

second command (after manchester decode):
00000000 0000 10101010 01 00000000 00000000 00000000 01 00000000 00000000 01 0000 01 00000000 00000000 0101010 0101010 01
(same as above just in groups of 8):
00000000            00001010    10100100    00000000 00000000 00000001 00000000 00000000 01000001 00000000 00000000     01010100 10101101
group_select_eq     address     mask        word ->                                                                     CRC
        so based on the mask, only:             ^               ^                           ^
                    are compared to the 8 bytes in the tag starting at 0x0a (the address)
0x00                0a          a4          00 00 01 00 00 41 00 00                                                     54 a9 after manchester decode








OK NOW FOR THE RECORDING WHERE I TRY TO CAPTURE THE TAG (April 23rd)

time plot shows serious mid-frequency component (based on period, looks to be about 1.25k?). I messed with the offset freq used for the xlating filter and confirmed adjusting it +/- a few kHz didn't fix it
I assume it's probably cause I had the rtl-sdr resting directly up against the car screen/toll tag while recording and it got recorded some noise
maybe try band reject filter?

set the time sink to collect a long time, like 10s worth of samples, then played around with different sections at different zoom levels
04-23 recording shows some command windows have more than 2 commands, meaning the reader is actually reading a tag that responded to the query commands!
interestingly enough it's the 6B/SeGo command sequence (short-long + others) that indicates a read, NOT the 6C command sequence (short-short)
some reads are short-long then 2xshort, some are short-long then 6xshort, very rarely s-l then 4xshort

s-l-4s:
- first of four:
    - preamble
    - check
    - 0000 1000 1001 1111 0000 0111
        - FAIL, crc
- second of four:
    - preamble
    - check
    - 0000 1001 1000 1111 0010 0110
        - SUCCESS, crc
- third of four:
    - preamble
    - check
    - 0000 1000 1001 1111 0000 0111
        - FAIL, crc
- fourth of four:
    - preamble
    - check
    - 0000 1001 1000 1111 0010 0110
        - SUCCESS, crc


2: fail, success
6: fail, success, fail, fail, success, success

looks like there is a slightly longer pause before fail then success, so visually can just tell based on timing

don't see tag response in what I looked at though, next steps:
- check the SeGo protocl document to make sure reader only sends fail/sucess if the tag sent something (make sure there is actually a needle in the haystack!)
- improve the flowgraph to decode each set of commands and write their samples to a file so I can better look for any interactions where I can actually see the tag response





general UHF RFID SDR links:
https://github.com/ransford/gen2_rfid
https://github.com/nkargas/Gen2-UHF-RFID-Reader
https://github.com/brunoprog64/rfid-gen2
https://www.slideshare.net/CNRFID/rfid-masterclass-2015

