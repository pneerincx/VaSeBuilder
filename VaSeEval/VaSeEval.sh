# Load the required tools and libraries.
ml BCFtools
ml VCFtools
ml ngs-utils
ml HTSlib
module list


# Create some needed variables. The first is the location of the 
donorVcfListFile="${1}"
ngsdnaVcf="${2}"
workingDir="${3}"
resultsVcf="${workingDir}/vaseresult.vcf.gz"


# Go to the working directory and copy the results VCF file there as we will be modifying it (filter out variants we don't need for the comparison).
cd "${workingDir}"
cp "${ngsdnaVcf} ${resultsVcf}"


# Create the temporary directory that will be used to create the combined VCF file
mkdir "${workingDir}/tmp"

# Create the file with the VaSe sample name that we will use to reheader the VCF
echo "VaSe" > "${workingDir}/tmp/vaseSample.txt"


# Read the donorvcf file (file containing a used donor files per sample) and copy the vcf files to a temporary directory as we will modify those as well (reheader).
dvFiles=( $(cut -f 2 ${donorVcfListFile}) )
for i in "${dvFiles[@]}"
do
	bcftools reheader -s "${workingDir}/tmp/vaseSample.txt" -o "${workingDir}tmp/${i}" "${i}"
done

# Concatenate all vcf.gz files into a vcf and compress it using bgzip from htslib.
vcf-concat "${workingDir}/tmp/*.vcf.gz" | bgzip > "${workingDir}/vaseeval.vcf.gz"

# Remove the INFO data from the combined VCF to avoid problems with the comparison
bcftools annotate -x INFO "${workingDir}/vaseeval.vcf.gz"


# Filter the vcf files to make the comparison easier
bcftools query -f '%CHROM\t%POS\n' "${workingDir}/vaseeval.vcf.gz" > "${workingDir}/vaseeval_chrompos.txt"
vcftools --positions "${workingDir}/vaseeval_chrompos.txt" --gzvcf "${resultsVcf}" --recode --out "${workingDir}/filtered_vaseresult"
mv "${workingDir}/filtered_vaseresult.recode.vcf" "${workingDir}/filtered_vaseresult.vcf"
bgzip "${workingDir}/filtered_vaseresult.vcf"


# Finally compare the two VCF files with vcf-compare_2
vcf-compare_2.0.sh -1 "${workingDir}/tmp/vaseeval.vcf.gz" -2 "${workingDir}/filtered_vaseresult.vcf.gz" -o "${workingDir}"


# Clean up afterwards (remove tmp dir and files)
rm -r "${workingDir}/tmp"
