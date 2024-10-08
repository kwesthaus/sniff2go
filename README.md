# sniff2go
Decode the ISO 18000-6B and -6C RF protocols used by the "GoodToGo!" tolling system in Washington and other states
See example recordings at https://zenodo.org/records/13346044.

## current state:

ROUGH WORK-IN-PROGRESS

## recordings
- 2 recordings on april 11th, when I drove on I-405. after tolling hours and I wasn't in the lane so my tag (probably) wasn't actually scanned
    - `gqrx_2-hot.raw` is the second recording, trimmed down to a period where the reader signal strength was really strong
- 1 recording on april 23rd, when I drove across 520 so my tag was definitely scanned

## reader demodulation/decoding
- have grc flowgraph to AM demod + show time plot for 2023-04-11 second recording, AND actually programatically extract SeGo bits (not 6C yet)

TODO:
    - extend flowgraph pipeline to 6C as well
    - copy trim flowgraph and apply to whole flowgraphs (for each recording)
        - might have to auto-adjust amplitude, clock

- when looking in time plot, short + short pulse is 6C, short + long pulse is 6B (SeGo)
- I used gnuradio time plot to manually confirm the 6C and SeGo trigger pulses (which are really full query commands, unlike the IAG trigger)
- I wrote python script to find extracted SeGo commands that don't match known values (init and select commands)

## tag demodulation/decoding
- copied reader flowgraph which just AM demods and shows time plot
- can see some 6B/SeGo interactions (not 6C) where there are additional commands beyond just the queries, manually decoded them to fail/success commands
- have yet to see tag response
    - some of the interference is just a weak signal from another reader

