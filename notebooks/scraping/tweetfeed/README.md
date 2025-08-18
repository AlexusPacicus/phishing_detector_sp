<div align="center">
    <h1 align="center">TweetFeed</h1>
    <h3 align="center">Feeds of IOCs posted by the community at Twitter</h3>

<p align="center">
    <b>
    <a href="https://tweetfeed.live">TweetFeed.live</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/0xDanielLopez/TweetFeed_code">Source code</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
    <a href="https://tweetfeed.live/feedback.html">Feedback</a>
    </b>
</p>

<h6 class="info-span">
    Want to integrate with OpenCTI? <a class="info-link" href="https://github.com/OpenCTI-Platform/connectors/tree/master/external-import/tweetfeed" target="_blank">Now you can!</a>
</h6>

---

  ![TweetFeed.live](https://user-images.githubusercontent.com/10616960/213568644-bb6b54b6-bd00-402e-b04f-266004b22d20.png)

---
</div>

## ☰ Content

- [Data collected](#page_facing_up-data-collected)
- [Some statistics](#bar_chart-some-statistics)
- [How it works](#question-how-it-works)
- [Hunting IOCs via Microsoft Defender](#mag-hunting-iocs-via-microsoft-defender)
- [Author](#bust_in_silhouette-author)
- [Disclaimer](#pushpin-disclaimer)

## :heart: Support the project
If you like the project, please consider:
- Giving it a star :star:
- Invite to a [coffee](https://www.buymeacoffee.com/dlopez) :coffee:

## :page_facing_up: Data collected
<div align="center">

<h3>Feeds</h3>

<table>
    <thead>
    </thead>
    <tbody>
    <tr>
        <th colspan=4>2025-08-04 10:18:26 (UTC)</th>
    </tr>
    <tr>
            <th>Today</th>
            <th>Last 7 days</th>
            <th>Last 30 days</th>
            <th>Last 365 days</th>
    </tr>
    <tr>
            <td>:clipboard: <a href="https://github.com/0xDanielLopez/TweetFeed/blob/master/today.csv">Today</a> (<a href="https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/today.csv">raw</a>)</td>
            <td>:clipboard: <a href="https://github.com/0xDanielLopez/TweetFeed/blob/master/week.csv">Week</a> (<a href="https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/week.csv">raw</a>)</td>
            <td>:clipboard: <a href="https://github.com/0xDanielLopez/TweetFeed/blob/master/month.csv">Month</a> (<a href="https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/month.csv">raw</a>)</td>
            <td>:clipboard: <a href="https://github.com/0xDanielLopez/TweetFeed/blob/master/year.csv">Year</a> (<a href="https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/year.csv">raw</a>)</td>
     </tr>
    </tbody>
</table>
</div>

<div align="center">

<h3>Output example</h3>

<table>
    <thead>
        <tr>
            <th><sub>Date (UTC)</sub></th>
            <th><sub>SourceUser</sub></th>
            <th><sub>Type</sub></th>
            <th><sub>Value</sub></th>
            <th><sub>Tags</sub></th>
            <th><sub>Tweet</sub></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><sub>2021-08-14 02:26:32</sub></td>
            <td><sub>phishunt_io</sub></td>
            <td><sub>url</sub></td>
            <td><sub>https://netflix.us2.cards/</sub></td>
            <td><sub>#phishing #scam</sub></td>
            <td><sub>https://twitter.com/phishunt_io/status/1426369619422502917</sub></td>
        </tr>
        <tr>
            <td><sub>2021-08-17 12:15:00</sub></td>
            <td><sub>TheDFIRReport</sub></td>
            <td><sub>ip</sub></td>
            <td><sub>185.56.76.94</sub></td>
            <td><sub>#Trickbot</sub></td>
            <td><sub>https://twitter.com/TheDFIRReport/status/1427604874053578756</sub></td>
        </tr>
    </tbody>
</table>
</div>

## :bar_chart: Some statistics

<div align="center">

<h3>Types</h3>

| Type | Today | Week | Month | Year |
| :--- | :---: | :---: | :---: | :---: |
| **:link: URLs** | 70 | 1071 | 5629 | 68921 |
| **:globe_with_meridians: Domains** | 57 | 513 | 2622 | 46933 |
| **:triangular_flag_on_post: IPs** | 13 | 480 | 2724 | 20498 |
| **:1234: SHA256** | 2 | 13 | 54 | 1634 |
| **:1234: MD5** | 6 | 82 | 291 | 2598 |

</div>

---

<div align="center">

<h3>Tags</h3>

| Tag | Today | Week | Month | Year |
| :--- | :---: | :---: | :---: | :---: |
| **#phishing** | 94 | 554 | 3671 | 83206 |
| **#scam** | 20 | 173 | 687 | 10057 |
| **#opendir** | 8 | 29 | 195 | 1037 |
| **#malware** | 0 | 74 | 379 | 21761 |
| **#maldoc** | 0 | 0 | 0 | 4 |
| **#ransomware** | 2 | 27 | 189 | 826 |
| **#banker** | 0 | 0 | 0 | 0 |
| **#AgentTesla** | 0 | 0 | 15 | 188 |
| **#Alienbot** | 0 | 0 | 0 | 0 |
| **#AsyncRAT** | 0 | 37 | 222 | 2506 |
| **#Batloader** | 0 | 0 | 0 | 0 |
| **#BazarLoader** | 0 | 0 | 0 | 0 |
| **#CobaltStrike** | 3 | 212 | 1344 | 9692 |
| **#Dcrat** | 0 | 8 | 47 | 347 |
| **#Emotet** | 0 | 0 | 0 | 0 |
| **#Formbook** | 18 | 114 | 159 | 431 |
| **#GootLoader** | 0 | 0 | 0 | 0 |
| **#GuLoader** | 0 | 6 | 7 | 43 |
| **#IcedID** | 0 | 0 | 0 | 0 |
| **#Lazarus** | 0 | 8 | 12 | 122 |
| **#Lokibot** | 0 | 4 | 6 | 125 |
| **#log4j** | 0 | 0 | 4 | 13 |
| **#Log4shell** | 0 | 0 | 0 | 0 |
| **#Njrat** | 4 | 26 | 111 | 1083 |
| **#Qakbot** | 0 | 32 | 149 | 891 |
| **#Raccoon** | 0 | 0 | 0 | 0 |
| **#RedLine** | 0 | 4 | 22 | 134 |
| **#Remcos** | 0 | 95 | 255 | 2590 |
| **#RaspberryRobin** | 0 | 0 | 0 | 0 |
| **#Spring4Shell** | 0 | 0 | 0 | 0 |
| **#SocGolish** | 0 | 0 | 0 | 7 |
| **#Ursnif** | 0 | 0 | 0 | 0 |

</div>

---

<div align="center">

<h3>Top Reporters (today)</h3>

| Number | User | IOCs | 
| :--- | :---: | :---: | 
| **#1** | [Metemcyber](https://twitter.com/Metemcyber) | 64 |
| **#2** | [skocherhan](https://twitter.com/skocherhan) | 20 |
| **#3** | [urldna_bot](https://twitter.com/urldna_bot) | 12 |
| **#4** | [catnap707](https://twitter.com/catnap707) | 10 |
| **#5** | [momomopas](https://twitter.com/momomopas) | 8 |
| **#6** | [@Phish_Destroy](https://twitter.com/@Phish_Destroy) | 6 |
| **#7** | [@CarlyGriggs13](https://twitter.com/@CarlyGriggs13) | 4 |
| **#8** | [@urldna_bot](https://twitter.com/@urldna_bot) | 2 |
| **#9** | [c9lab_soc](https://twitter.com/c9lab_soc) | 4 |
| **#10** | [G60930953](https://twitter.com/G60930953) | 3 |

</div>

## :question: How it works?
Search tweets that contain certain tags **or** that are posted by certain *infosec* people.

### Tags being searched
##### *(not case sensitive)*
```
- #phishing
- #scam
- #opendir
- #malware
- #maldoc
- #ransomware
- #banker
- #AgentTesla
- #Alienbot
- #AsyncRAT
- #BazarLoader
- #Batloader
- #CobaltStrike
- #Dcrat
- #Emotet
- #Formbook
- #GootLoader
- #GuLoader
- #IcedID
- #Lazarus
- #Lokibot
- #log4j
- #Log4shell
- #Njrat
- #Qakbot
- #Raccoon
- #RedLine
- #Remcos
- #RaspberryRobin
- #Spring4Shell
- #SocGholish
- #Ursnif
```


### Also search Tweets posted by
##### *(these are trusted folks that sometimes don't use tags)*
<big><pre>
[**TweetFeed list**](https://twitter.com/i/lists/1423693426437001224)
</pre></big>

## :mag: Hunting IOCs via Microsoft Defender

**1. Search `SHA256` hashes with `yearly` tweets feed**
```kusto
let MaxAge = ago(30d);
let SHA256_whitelist = pack_array(
'XXX' // Some SHA256 hash you want to whitelist.
);
let TweetFeed = materialize (
    (externaldata(report:string)
    [@"https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/year.csv"]
    with (format = "txt"))
    | extend report = parse_csv(report)
    | extend Type = tostring(report[2])
    | where Type == 'sha256'
    | extend SHA256 = tostring(report[3])
    | where SHA256 !in(SHA256_whitelist)
    | extend Tag = tostring(report[4])
    | extend Tweet = tostring(report[5])
    | project SHA256, Tag, Tweet 
);
union (
    TweetFeed
    | join (
        DeviceProcessEvents
        | where Timestamp > MaxAge
    ) on SHA256
), (
    TweetFeed
    | join (
        DeviceFileEvents
        | where Timestamp > MaxAge
    ) on SHA256
), ( 
    TweetFeed
    | join (
        DeviceImageLoadEvents
        | where Timestamp > MaxAge
    ) on SHA256
) | project Timestamp, DeviceName, FileName, FolderPath, SHA256, Tag, Tweet
```

<br>

**2. Search `IP addresses` with `monthly` tweets feed**
```kusto
let MaxAge = ago(30d);
let IPaddress_whitelist = pack_array(
'XXX' // Some IP address you want to whitelist.
);
let TweetFeed = materialize (
    (externaldata(report:string)
    [@"https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/month.csv"]
    with (format = "txt"))
    | extend report = parse_csv(report)
    | extend Type = tostring(report[2])
    | where Type == 'ip'
    | extend RemoteIP = tostring(report[3])
    | where RemoteIP !in(IPaddress_whitelist)
    | where not(ipv4_is_private(RemoteIP))
    | extend Tag = tostring(report[4])
    | extend Tweet = tostring(report[5])
    | project RemoteIP, Tag, Tweet 
);
union (
TweetFeed
    | join (
        DeviceNetworkEvents
    | where Timestamp > MaxAge
    ) on RemoteIP
) | project Timestamp, DeviceName, RemoteIP, Tag, Tweet
```

<br>

**3. Search `urls` and `domains` with `weekly` tweets feed**
```kusto
let MaxAge = ago(30d);
let domain_whitelist = pack_array(
'XXX' // Some URL/Domain you want to whitelist.
);
let TweetFeed = materialize (
    (externaldata(report:string)
    [@"https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/week.csv"]
    with (format = "txt"))
    | extend report = parse_csv(report)
    | extend Type = tostring(report[2])
    | where Type in('url','domain')
    | extend RemoteUrl = tostring(report[3])
    | where RemoteUrl !in(domain_whitelist)
    | extend Tag = tostring(report[4])
    | extend Tweet = tostring(report[5])
    | project RemoteUrl, Tag, Tweet 
);
union (
TweetFeed
    | join (
        DeviceNetworkEvents
    | where Timestamp > MaxAge
    ) on RemoteUrl
) | project Timestamp, DeviceName, RemoteUrl, Tag, Tweet
```

## :bust_in_silhouette: Author
* [**Daniel López**](https://twitter.com/0xDanielLopez)

<!--- ![Twitter](https://img.icons8.com/officexs/16/000000/twitter.png) --->

## :pushpin: Disclaimer

Please note that all the data is collected from Twitter and sorted/served here as it is on **best effort**.

I have tried to tune as much as possible the searches trying to collect only valuable info. However please consider making your own analysis before taking any action related to these IOCs.

Anyway feel free to **[reach me out](https://twitter.com/0xDanielLopez)** or to provide any kind of **[feedback](https://tweetfeed.live/feedback.html)** regarding any contribution or suggestion.

<hr>

<b>By the community, for the community.</b>