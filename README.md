# bme590hrm
MIT License

Copyright (c) 2017 Daniel Wu, Samuel Li, Brianna Loomis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Primary functionality in hrm.py <br />
Main calls associated subfunctions: peak detection, bradycardia/
tachycardia detection, and instantaneous/average heartrate detection. <br />
hrm.py main creates and writes to a file "testfile.txt", added calculated
values for instantaneous heartrate, average heartrate, and whether anomalies
were detected.

Run instructions:
Call hrm.py with single .csv file and specified values for time range for
average heartrate, bradycardia thresholds, and tachycardia thresholds.
Default values exist.

Notes: "times" and "voltages" must be specified in the first two rows of the
header for the csv. Outputs for the averages and instantaneous heartrates are
given in bpm. For brady and tachy, the outputs are given in seconds.