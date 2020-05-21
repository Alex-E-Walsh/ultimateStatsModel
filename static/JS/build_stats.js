
  function cleanStat(stat){
    stat = stat.split(",")
    stat.pop()
    stat[0] = stat[0].slice(16)
    stat[18] = stat[18].slice(1,6)
    stat = stat.map(Number)
    return stat
  }
  var homevals = cleanStat(document.getElementById('stathome').innerText)
  var awayvals = cleanStat(document.getElementById('stataway').innerText)

  var hometeam = document.getElementById('result').innerText.split(" ")[0].split('\n')[1]
  var awayteam = document.getElementById('result').innerText.split(" ")[3]

    // document.getElementById('cols').innerHTML = (
    //   `<th>Team</th>
    //   <th>G</th>
    //   <th>W</th>
    //   <th>L</th>
    //   <th>T</th>
    //   <th>PTS</th>
    //   <th>PPG</th>
    //   <th>PA</th>
    //   <th>PAPG</th>
    //   <th>OEFF</th>
    //   <th>DEFF</th>
    //   <th>+/-</th>
    //   <th>+/- PG</th>
    //   <th>BLK</th>
    //   <th>BPG</th>
    //   <th>CMP</th>
    //   <th>CPG</th>
    //   <th>CMP%</th>
    //   <th>TO</th>
    //   <th>TPG</th>`)

  function makeTable(){
    document.getElementById('awayteam').innerHTML
    document.getElementById('homestat').insertCell(0).innerHTML = hometeam
    document.getElementById('awaystat').insertCell(0).innerHTML = awayteam
    for(let i =0;i<homevals.length;i++){
        document.getElementById('homestat').insertCell(i+1).innerHTML = homevals[i]
        document.getElementById('awaystat').insertCell(i+1).innerHTML = awayvals[i]
      }
    };

  makeTable();
