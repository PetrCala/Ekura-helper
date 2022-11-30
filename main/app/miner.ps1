[System.Reflection.Assembly]::LoadWithPartialName("PresentationFramework") | Out-Null

function Import-Xaml {
	[xml]$xaml = Get-Content -Path $PSScriptRoot\miner.xaml
	$manager = New-Object System.Xml.XmlNamespaceManager -ArgumentList $xaml.NameTable
	$manager.AddNamespace("x", "http://schemas.microsoft.com/winfx/2006/xaml");
	$xamlReader = New-Object System.Xml.XmlNodeReader $xaml
	[Windows.Markup.XamlReader]::Load($xamlReader)
}
$Window = Import-Xaml #Assigns the output of the Import-Xaml function to a variable called Window

$Find = $Window.FindName("Find")
$Mine = $Window.FindName("Mine")
$Stop = $Window.FindName("Stop")
$Processlist = $Window.FindName("Processlist")

$Find.add_Click({ #Gets added once Find is clicked
    $Find.Content = "Hello" #Update content of the button
})

#Trying to run the .cs script
$source = Get-Content -Path $PSScriptRoot\test.cs
Add-Type -TypeDefinition $source
[Test]::ExampleFunction()


#Call a  static method





$Window.ShowDialog()