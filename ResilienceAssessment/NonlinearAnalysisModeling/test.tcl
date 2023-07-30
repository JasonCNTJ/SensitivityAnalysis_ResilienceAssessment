# Define analysis series
set AnalysisLoadType [list EigenValue DeadLoad LiveLoad EarthquakeLoad GravityEarthquake]

# Loop over all the analysis types
foreach LoadType $AnalysisLoadType {

puts "Analysis type is $LoadType"

}