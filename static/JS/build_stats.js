$(document).ready(function () {


  function cleanStat(stat){
    stat = stat.split(",")
    stat.pop()
    stat[0] = stat[0].slice(17)
    stat[18] = stat[18].slice(3,8)
    stat = stat.map(Number)
    return stat
  }

  var homevals = cleanStat($('#stathome').text())
  var awayvals = cleanStat($('#stataway').text())


  function buildTableRow(arr){
    rowHTML = []
    for(let i =0;i<arr.length;i++){
      var td = "".concat("<td>",arr[i],"<td>")
      rowHTML.push(td)
    }
    return rowHTML
  }


    $('#cols').html(
      `<th>G</th>
      <th>W</th>
      <th>L</th>
      <th>T</th>
      <th>PTS</th>
      <th>PPG</th>
      <th>PA</th>
      <th>PAPG</th>
      <th>OEFF</th>
      <th>DEFF</th>
      <th>+/-</th>
      <th>+/- PG</th>
      <th>BLK</th>
      <th>BPG</th>
      <th>CMP</th>
      <th>CPG</th>
      <th>CMP%</th>
      <th>TO</th>
      <th>TPG</th>`)

    console.log(buildTableRow(homevals))
    $('#homestat').html(buildTableRow(homevals))

    $('#awaystat').html(buildTableRow(awayvals))
    })
