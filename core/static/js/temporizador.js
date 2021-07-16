var yourDateToGo = new Date(); //here you're making new Date object
    yourDateToGo.setDate(yourDateToGo.getDate() + 1); //your're setting date in this object 1 day more from now
    //you can change number of days to go by putting any number in place of 1

    var timing = setInterval( // you're making an interval - a thing, that is updating content after number of miliseconds, that you're writing after comma as second parameter
      function () {

        var currentDate = new Date().getTime(); //same thing as above
        var timeLeft = yourDateToGo - currentDate; //difference between time you set and now in miliseconds

        var days = Math.floor(timeLeft / (1000 * 60 * 60 * 24)); //conversion miliseconds on days 
        if (days < 10) days="0"+days; //if number of days is below 10, programm is writing "0" before 9, that's why you see "09" instead of "9"
        var hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)); //conversion miliseconds on hours
        if (hours < 10) hours="0"+hours;
        var minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60)); //conversion miliseconds on minutes 
        if (minutes < 10) minutes="0"+minutes;
        var seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);//conversion miliseconds on seconds
        if (seconds < 10) seconds="0"+seconds;

        document.getElementById("countdown").innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s"; // putting number of days, hours, minutes and seconds in div, 
        //which id is countdown

        if (timeLeft <= 0) {
          clearInterval(timing);
          document.getElementById("countdown").innerHTML = "It's over"; //if there's no time left, programm in this 2 lines is clearing interval (nothing is counting now) 
          //and you see "It's over" instead of time left
        }
      }, 1000);

      function firstExample () {

        for(;;) {
        var x = prompt("Enter number of days");
        x = parseInt(x);
        if (x>0 && x<30) break;
        else alert("Enter number between 0 and 30")

        }
       

        var yourDateToGo2 = new Date();
        yourDateToGo2.setDate(yourDateToGo2.getDate() + x);

        var timing2 = setInterval(
      function () {

        var currentDate2 = new Date().getTime();
        var timeLeft2 = yourDateToGo2 - currentDate2; 

        var days2 = Math.floor(timeLeft2 / (1000 * 60 * 60 * 24));
        if (days2 < 10) days2="0"+days2; 
        var hours2 = Math.floor((timeLeft2 % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        if (hours2 < 10) hours2="0"+hours2;
        var minutes2 = Math.floor((timeLeft2 % (1000 * 60 * 60)) / (1000 * 60));  
        if (minutes2 < 10) minutes2="0"+minutes2;
        var seconds2 = Math.floor((timeLeft2 % (1000 * 60)) / 1000);
        if (seconds2 < 10) seconds2="0"+seconds2;

        document.getElementById("countdown2").innerHTML = days2 + "d " + hours2 + "h " + minutes2 + "m " + seconds2 + "s";  
        

        if (timeLeft2 <= 0) {
          clearInterval(timing2);
          document.getElementById("countdown2").innerHTML = "It's over"; 
          
        }
      }, 1000);

      }
document.getElementById('btnId').addEventListener('click', firstExample);
