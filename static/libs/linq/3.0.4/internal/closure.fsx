<<<<<<< HEAD
﻿open System
open System.IO
open System.Text
open System.Diagnostics

// working...

let args = ["-jar", "lib/compiler.jar";
            "--compilation_level", "ADVANCED_OPTIMIZATIONS";
            "--warning_level", "VERBOSE";
            "--externs", "externs.js";
            "--jscomp_error", "checkTypes"
            "--js_output_file", "linq.closureoptimization.js"];



let inputs =
    ["../linq.js"; "test.js"]
    |> List.map (fun x -> ("--js", x))

new ProcessStartInfo(
    FileName = "java",
    Arguments = (args @ inputs |> Seq.map (fun (x,y) -> x + " " + y) |> String.concat " "),
    RedirectStandardOutput = true,
    UseShellExecute = false,
    WorkingDirectory = __SOURCE_DIRECTORY__)
|> Process.Start
=======
﻿open System
open System.IO
open System.Text
open System.Diagnostics

// working...

let args = ["-jar", "lib/compiler.jar";
            "--compilation_level", "ADVANCED_OPTIMIZATIONS";
            "--warning_level", "VERBOSE";
            "--externs", "externs.js";
            "--jscomp_error", "checkTypes"
            "--js_output_file", "linq.closureoptimization.js"];



let inputs =
    ["../linq.js"; "test.js"]
    |> List.map (fun x -> ("--js", x))

new ProcessStartInfo(
    FileName = "java",
    Arguments = (args @ inputs |> Seq.map (fun (x,y) -> x + " " + y) |> String.concat " "),
    RedirectStandardOutput = true,
    UseShellExecute = false,
    WorkingDirectory = __SOURCE_DIRECTORY__)
|> Process.Start
>>>>>>> 9fe5041adb8bd46e6986e2837e2f09061ff40e0d
|> fun p -> Console.WriteLine(p.StandardOutput.ReadToEnd())