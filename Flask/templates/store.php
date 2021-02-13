<?php
    $myfile = fopen("Output.txt", "a+");
    $txt = "".$_POST['edit'];
    fwrite($myfile, $txt);
    fclose($myfile);
?>