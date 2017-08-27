function mtofeet(x) {return 3.2808399 * x;}

function intcomma(x) {return x.replace(/\B(?=(\d{3})+(?!\d))/g, ",");}

var right_ascension = {}
var declination = {}

window.onload = function init_ra_dec_arrays() {
    alltables = document.getElementsByTagName('table')
    for (var i = 0; i < alltables.length; i++) {
        var table = alltables[i]
        var rah_list = []
        var rahms_list = []
        var decdeg_list = []
        var decdms_list = []
        for (var j = 1, row; row = table.rows[j]; j++) {
            // Push Right Ascensions
            rah = row.cells[2].innerHTML
            rahms = raDeg2Hms(rah * 15)
            rah_list.push(rah)
            rahms_list.push(rahms)
            // Push Declinations
            decdeg = row.cells[3].innerHTML
            decdms = decDeg2Hms(decdeg)
            decdeg_list.push(decdeg)
            decdms_list.push(decdms)
        }
        right_ascension[alltables[i].id] = {
            'hour': rah_list,
            'hms': rahms_list,
        }
        declination[alltables[i].id] = {
            'degree': decdeg_list,
            'dms': decdms_list,
        }
    }
}

function decDeg2Hms(dec) {
  var prefix = ''
  var deg = +dec
  if (deg < 0) {
    prefix = '-'
    deg = Math.abs(deg)
  }
  var hour = Math.floor(deg)
  var min = Math.abs(Math.floor((deg - hour) * 60))
  var sec = (Math.abs((deg - hour) * 60) - min) * 60
  sec = Math.floor(sec)
  return prefix + [hour, min, sec].join(':')
}

function decHms2Deg(dec, round) {
  var parts = dec.split(':')
  var sign = 1
  var d = parseFloat(parts[0])
  var m = parseFloat(parts[1])
  var s = parseFloat(parts[2])
  if (d.toString()[0] === '-') {
    sign = -1
    d = Math.abs(d)
  }
  var sDeg = (s / 3600)
  if (round) sDeg = Math.floor(sDeg)
  var deg = d + (m / 60) + sDeg
  return deg * sign
}

function raDeg2Hms(ra) {
    var prefix = ''
    var deg = +ra
    if (deg < 0) {
        prefix = '-'
        deg = Math.abs(deg)
    }
    var hour = Math.floor(deg / 15)
    var min = Math.floor(((deg / 15) - hour) * 60)
    var sec = ((((deg / 15) - hour) * 60) - min) * 60
    sec = Math.floor(sec * 100) / 100
    return prefix + [hour, min, sec].join(':')
}

function raHms2Deg(ra, round) {
  var parts = ra.split(':')
  var sign = 1
  var h = parseFloat(parts[0])
  var m = parseFloat(parts[1])
  var s = parseFloat(parts[2])
  if (h.toString()[0] === '-') {
    sign = -1
    h = Math.abs(h)
  }
  var sDeg = (s / 240)
  if (round) sDeg = Math.floor(sDeg)
  deg = (h * 15) + (m / 4) + sDeg
  return deg * sign
}

function set_column_ra_hms(table_id) {
    var table = document.getElementById(table_id);
    for (var i = 1, row; row = table.rows[i]; i++) {
        row.cells[2].innerHTML = right_ascension[table_id]['hms'][i - 1]
    }
}

function set_column_ra_hourangle(table_id) {
    var table = document.getElementById(table_id);
    for (var i = 1, row; row = table.rows[i]; i++) {
        row.cells[2].innerHTML = right_ascension[table_id]['hour'][i - 1]
    }
}

function set_column_dec_degree(table_id) {
    var table = document.getElementById(table_id);
    for (var i = 1, row; row = table.rows[i]; i++) {
        row.cells[3].innerHTML = declination[table_id]['degree'][i - 1]
    }
}

function set_column_dec_dms(table_id) {
    var table = document.getElementById(table_id);
    for (var i = 1, row; row = table.rows[i]; i++) {
        row.cells[3].innerHTML = declination[table_id]['dms'][i - 1]
    }
}
