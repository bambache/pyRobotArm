<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<title> pyRobotArm Web</title>
  
<style type='text/css'>
    input[type="range"] {
    position:relative;
    -webkit-transform: rotate(90deg);
    top:100px;
    }
</style>

</head>
<body>

<p>Use sliders to move robotic arm (values are in degrees 90 being the middle):</p>
%for idx in range(len(values)):
<input id="slider{{idx}}" type="range" name="points" value="{{values[idx]}}" min="0" max="180">
%end

</body>
</html>

