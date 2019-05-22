import logging
import statistics
from OverlapContext import OverlapContext
from VariantContext import VariantContext


class VariantContextFile:
    def __init__(self, fileloc=None, samplefilter=None,
                 varconfilter=None, chromfilter=None):
        self.vaselogger = logging.getLogger("VaSe_Logger")
        self.variant_context_file_location = fileloc
        self.variant_contexts = {}
        self.variant_context_statistics = None
        self.varcon_fields = {1: "variant context id",
                              2: "sample id",
                              3: "chromosome",
                              4: "origin",
                              5: "start pos",
                              6: "end pos",
                              7: "acceptor context",
                              8: "donor context",
                              9: "number of acceptor reads",
                              10: "number of donor reads",
                              11: "acceptor/donor ratio",
                              12: "acceptor read ids",
                              13: "donor read ids"}
        if fileloc is not None:
            # Read the provided variant context file with set optional
            # filters.
            self.read_variant_context_file(fileloc, samplefilter,
                                           varconfilter, chromfilter)

    # ===METHODS TO GET DATA FROM THE VARIANT CONTEXT FILE=====================
    def get_variant_contexts(self, asdict=False):
        if asdict:
            return self.variant_contexts
        return [varcon for varcon in self.variant_contexts.values()]

    def get_variant_context_ids(self):
        return [x for x in self.variant_contexts.keys()]

    # Returns a specified variant context.
    def get_variant_context(self, contextid):
        if contextid in self.variant_contexts:
            return self.variant_contexts[contextid]
        return None

    # Returns the acceptor context of the specified variant context.
    def get_acceptor_context(self, contextid):
        if contextid in self.variant_contexts:
            return self.variant_contexts[contextid].get_acceptor_context()
        return None

    # Returns the donor context of the specified variant context.
    def get_donor_context(self, contextid):
        if contextid in self.variant_contexts:
            return self.variant_contexts[contextid].get_donor_context()
        return None

    # Returns all variant context acceptor reads.
    def get_all_variant_context_acceptor_reads(self):
        acceptorreads = []
        for varcon in self.variant_contexts.values():
            acceptorreads.extend(varcon.get_acceptor_reads())
        return acceptorreads

    # Returns all variant context donor reads.
    def get_all_variant_context_donor_reads(self):
        donorreads = []
        for varcon in self.variant_contexts.values():
            donorreads.extend(varcon.get_donor_reads())
        return donorreads

    # Returns all variant context acceptor read ids.
    def get_all_variant_context_acceptor_read_ids(self):
        acceptorreadids = []
        for varcon in self.variant_contexts.values():
            acceptorreadids.extend(varcon.get_acceptor_read_ids())
        return acceptorreadids

    # Returns the variant context donor read ids.
    def get_all_variant_context_donor_read_ids(self):
        donorreadids = []
        for varcon in self.variant_contexts.values():
            donorreadids.extend(varcon.get_donor_read_ids())
        return donorreadids

    # ===BASIC VARIANTCONTEXTFILE METHODS======================================
    # Reads a provided variant context file and saves data according to
    # set filters.
    def read_variant_context_file(self, fileloc, samplefilter=None,
                                  varconfilter=None, chromfilter=None):
        try:
            with open(fileloc, "r") as vcFile:
                next(vcFile)    # Skip the header line.
                for fileline in vcFile:
                    fileline = fileline.strip()
                    filelinedata = fileline.split("\t")

                    samplepass = self.passes_filter(filelinedata[1],
                                                    samplefilter)
                    varconpass = self.passes_filter(filelinedata[0],
                                                    varconfilter)
                    chrompass = self.passes_filter(filelinedata[2],
                                                   chromfilter)

                    if samplepass and varconpass and chrompass:
                        varconObj = None
                        if (self.variantContextFileType == "acceptor"
                           or self.variantContextFileType == "donor"):
                            varconObj = VariantContext(
                                    self.variantContextFileType,
                                    filelinedata[0],
                                    filelinedata[1],
                                    filelinedata[2],
                                    int(filelinedata[3]),
                                    int(filelinedata[4]),
                                    int(filelinedata[5]),
                                    filelinedata[7].split(";")
                                    )
                        else:
                            varconObj = varconObj = VariantContext(
                                    self.variantContextFileType,
                                    filelinedata[0],
                                    filelinedata[1],
                                    filelinedata[2],
                                    int(filelinedata[3]),
                                    int(filelinedata[4]),
                                    int(filelinedata[5]),
                                    int(filelinedata[6]),
                                    int(filelinedata[7]),
                                    int(filelinedata[8]),
                                    int(filelinedata[9]),
                                    float(filelinedata[10]),
                                    filelinedata[11].split(";"),
                                    filelinedata[12].split(";")
                                    )
                        if (filelinedata[1] not in self.variantContextsBySample):
                            self.variantContextsBySample[filelinedata[1]] = []
                        self.variantContextsBySample[filelinedata[1]].append(varconObj)
                        self.variantContextsById[filelinedata[0]] = varconObj
                        self.variant_contexts.append(varconObj)
        except IOError as ioe:
            self.vaselogger.critical("Could not read varcon file "
                                     f"{ioe.filename}")

    # Returns whether something is in the filter or not.
    def passes_filter(self, valtocheck, filterlist):
        if filterlist is not None:
            return valtocheck in filterlist
        return True

    # ===VARIANT CONTEXT SET OPERATIONS (UNION, INTERSECT, DIFFERENCE)=========
    # Returns the list of variant context identifiers from both variant
    # context files.
    def get_variant_contexts_union(self, other_varcon_file):
        own_varcon_ids = self.get_variant_context_ids()
        other_varcon_ids = other_varcon_file.get_variant_context_ids()
        return list(set(own_varcon_ids) | set(other_varcon_ids))

    # Returns the list of variant context identifiers present in both
    # variant context files.
    def get_variant_contexts_intersect(self, other_varcon_file):
        own_varcon_ids = self.get_variant_context_ids()
        other_varcon_ids = other_varcon_file.get_variant_context_ids()
        return list(set(own_varcon_ids) & set(other_varcon_ids))

    # Returns the list of variant context identifiers in this file but
    # not present in the other variant context file.
    def get_variant_contexts_difference(self, other_varcon_file):
        own_varcon_ids = self.get_variant_context_ids()
        other_varcon_ids = other_varcon_file.get_variant_context_ids()
        return list(set(own_varcon_ids) - set(other_varcon_ids))

    # Returns the list of variant context identifiers only present in
    # one of the variant context file but not the other.
    def get_variant_contexts_symmetric_difference(self, other_varcon_file):
        own_varcon_ids = self.get_variant_context_ids()
        other_varcon_ids = other_varcon_file.get_variant_context_ids()
        return list(set(own_varcon_ids) ^ set(other_varcon_ids))

    # ===METHODS TO OBTAIN VARIANT CONTEXT DATA BASED ON FILTERS===============
    # Returns a list/hashmap of VariantContextObjects.
    def get_variant_contexts2(self, aslist=False, varconfilter=None,
                              samplefilter=None, chromfilter=None):
        if aslist:
            return [
                    x for x in self.variant_contexts.values()
                    if (self.passes_filter(x.get_variant_context_id(),
                                           varconfilter)
                        and self.passes_filter(x.get_variant_context_sample(),
                                               samplefilter)
                        and self.passes_filter(x.get_variant_context_chrom(),
                                               chromfilter))
                    ]
        return {
                k: v for k, v in self.variant_contexts
                if (self.passes_filter(k, varconfilter)
                    and self.passes_filter(v.get_variant_context_sample(),
                                           samplefilter)
                    and self.passes_filter(v.get_variant_context_chrom(),
                                           chromfilter))
                }

    # ====METHODS TO ASSESS WHETHER A VARIANT IS IN AN EXISTING CONTEXT========
    # Main method that returns whether a variant (SNP or indel).
    def variant_is_in_context(self, varianttype, searchchrom,
                              searchstart, searchstop):
        if varianttype == "snp":
            return self.snp_variant_is_in_context(searchchrom, searchstart)
        if varianttype == "indel":
            return self.indel_variant_is_in_context(searchchrom, searchstart,
                                                    searchstop)
        return None

    # Determines whether an SNP variant is located in an already
    # existing variant context.
    def snp_variant_is_in_context(self, varchrom, vcfvarpos):
        for varcon in self.variant_contexts.values():
            if varchrom == varcon.get_variant_context_chrom():
                if (vcfvarpos >= varcon.get_variant_context_start()
                   and vcfvarpos <= varcon.get_variant_context_end()):
                    return True
        return False

    # Determines whether an indel variant is located within an existing
    # variant context (indelLeftPos and indelRightPos can be the used
    # search window).
    def indel_variant_is_in_context(self, indelchrom, indelleftpos, indelrightpos):
        for varcon in self.variant_contexts.values():
            if (indelchrom == varcon.get_variant_context_chrom()):
                if (indelleftpos <= varcon.get_variant_context_start()
                   and indelrightpos >= varcon.get_variant_context_start()):
                    return True
                if (indelleftpos <= varcon.get_variant_context_end()
                   and indelrightpos >= varcon.get_variant_context_end()):
                    return True
                if (indelleftpos >= varcon.get_variant_context_start()
                   and indelrightpos <= varcon.get_variant_context_end()):
                    return True
        return False

    # ===METHODS TO ADD DATA/VARIANT CONTEXTS TO THE VARIANT CONTEXT FILE======
    # Sets a variant context object to a specified context id.
    def set_variant_context(self, varconid, varcontext):
        self.variant_contexts[varconid] = varcontext

    # Adds a variant context object
    def add_variant_context(self, varconid, sampleid,
                            varconchrom, varconorigin,
                            varconstart, varconend,
                            varcon_areads, varcon_dreads,
                            acceptor_context=None, donor_context=None):
        varcon_obj = VariantContext(varconid, sampleid,
                                    varconchrom, varconorigin,
                                    varconstart, varconend,
                                    varcon_areads, varcon_dreads,
                                    acceptor_context, donor_context)
        self.variant_contexts[varconid] = varcon_obj

    # Adds an acceptor context object to a variant context.
    def set_acceptor_context(self, varconid, acceptor_context):
        if varconid in self.variant_contexts:
            self.variant_contexts[varconid].set_acceptor_context(acceptor_context)

    # Add a newly created acceptor context to an existing variant
    # context.
    def add_acceptor_context(self, contextid, sampleid,
                             contextchrom, contextorigin,
                             contextstart, contextend,
                             acceptorreads):
        if contextid in self.variant_contexts:
            self.variant_contexts[contextid].add_acceptor_context(
                    contextid, sampleid,
                    contextchrom, contextorigin,
                    contextstart, contextend,
                    acceptorreads)

    # Sets the donor context object of a variant context
    def set_donor_context(self, varconid, donor_context):
        if varconid in self.variant_contexts:
            self.variant_contexts[varconid].set_donor_context(donor_context)

    # Add a newly created donor context to an existing variant context.
    def add_donor_context(self, contextid, sampleid,
                          contextchrom, contextorigin,
                          contextstart, contextend,
                          donorreads):
        if contextid in self.variant_contexts:
            self.variant_contexts[contextid].add_donor_context(
                    contextid, sampleid,
                    contextchrom, contextorigin,
                    contextstart, contextend,
                    donorreads)

    # ===METHODS TO ADD UNMAPPED MATE IDS TO ACCEPTOR, DONOR AND VARIANT=======
    # ===CONTEXT===
    # Sets the unmapped mate read id for a specified acceptor context.
    def set_acceptor_context_unmapped_mate_ids(self, contextid, mateids):
        if contextid in self.variant_contexts:
            self.variant_contexts[contextid].set_acceptor_context_unmapped_mates(mateids)

    # Sets the unmapped mate read id for a specified donor context.
    def set_donor_context_unmapped_mate_ids(self, contextid, mateids):
        if contextid in self.variant_contexts:
            self.variant_contexts[contextid].set_donor_context_unmapped_mates(mateids)

    # Sets the acceptor unmapped mate ids for a specified variant
    # context.
    def set_unmapped_acceptor_mate_ids(self, contextid, mateids):
        if contextid in self.variant_contexts:
            self.variant_contexts[contextid].set_unmapped_acceptor_mate_ids(mateids)

    # Sets the donor unmapped mate ids for a specified variant context.
    def set_unmapped_donor_mate_ids(self, contextid, mateids):
        if contextid in self.variant_contexts:
            self.variant_contexts[contextid].set_unmapped_donor_mate_ids(mateids)

    # ===METHODS TO GET UNMAPPED MATE IDS OF AN ACCEPTOR, DONOR AND============
    # ===VARIANT CONTEXT===
    # Return the unmapped read mate identifiers of a specified acceptor
    # context.
    def get_acceptor_context_unmapped_mate_ids(self, contextid):
        if contextid in self.variant_contexts:
            return self.variant_contexts[contextid].get_acceptor_context_unmapped_mate_ids()
        return []

    # Returns the unmapped read mate identifiers of a specified donor
    # context.
    def get_donor_context_unmapped_mate_ids(self, contextid):
        if contextid in self.variant_contexts:
            return self.variant_contexts[contextid].get_donor_context_unmapped_mate_ids()
        return []

    # Returns the unmapped acceptor read mate identifiers of a specified
    # variant context.
    def get_unmapped_acceptor_mate_ids(self, contextid):
        if contextid in self.variant_contexts:
            return self.variant_contexts[contextid].get_unmapped_acceptor_read_ids()
        return []

    # Returns the unmapped donor read mate identifiers of a specified
    # variant context.
    def get_unmapped_donor_mate_ids(self, contextid):
        if contextid in self.variant_contexts:
            return self.variant_contexts[contextid].get_unmapped_donor_read_ids()
        return []

    # ===METHODS TO OBTAIN SOME STATISTICS ABOUT ALL THE CONTEXTS==============
    # Returns the average variant context length within this variant
    # context file.
    def get_average_variant_context_length(self):
        return statistics.mean([varcon.get_variant_context_length()
                                for varcon in self.variant_contexts.values()])

    # Returns the median variant context length within this variant
    # context file.
    def get_median_variant_context_length(self):
        return statistics.median([varcon.get_variant_context_length()
                                  for varcon in self.variant_contexts.values()])

    # Returns the average number of variant context reads for this
    # variant context file.
    def get_average_variant_context_reads(self):
        return statistics.mean()

    # Returns the median number of variant context reads for this
    # variant context file.
    def get_median_variant_context_reads(self):
        return statistics.median()

    # ===METHODS TO WRITE VARIANT CONTEXT DATA TO A FILE=======================
    # Writes the variant context data to an output file.
    def write_variant_context_file(self, outfileloc, samplefilter=None,
                                   varconfilter=None, chromfilter=None):
        try:

            with open(outfileloc, "w") as varcon_outfile:
                varcon_outfile.write("#ContextId\tDonorSample\tChrom\tOrigin\t"
                                     "Start\tEnd\tAcceptorContextLength\t"
                                     "DonorContextLength\tAcceptorReads\t"
                                     "DonorReads\tADratio\tAcceptorReadsIds\t"
                                     "DonorReadIds\n")
                for varcon in self.variant_contexts.values():
                    samplepass = self.passes_filter(
                            varcon.get_variant_context_sample(),
                            samplefilter
                            )
                    varconpass = self.passes_filter(
                            varcon.get_variant_context_id(),
                            varconfilter
                            )
                    chrompass = self.passes_filter(
                            varcon.get_variant_context_chrom(),
                            chromfilter
                            )
                    if samplepass and varconpass and chrompass:
                        varcon_outfile.write(varcon.to_string() + "\n")
        except IOError as ioe:
            self.vaselogger.warning("Could not write variant contexts to "
                                    f"{ioe.filename}")

    # Writes the donor contexts used to construct the variant contexts.
    def write_acceptor_context_file(self, outfileloc, samplefilter=None,
                                    contextfilter=None, chromfilter=None):
        try:
            with open(outfileloc, "w") as varcon_oufile:
                varcon_oufile.write("#ContextId\tDonorSample\tChrom\tOrigin\t"
                                    "Start\tEnd\tNumOfReads\tReadIds\n")
                for varcon in self.variant_contexts.values():
                    samplepass = self.passes_filter(
                            varcon.get_variant_context_sample(),
                            samplefilter
                            )
                    varconpass = self.passes_filter(
                            varcon.get_variant_context_id(),
                            contextfilter
                            )
                    chrompass = self.passes_filter(
                            varcon.get_variant_context_chrom(),
                            chromfilter
                            )
                    if samplepass and varconpass and chrompass:
                        varcon_oufile.write(
                            varcon.get_acceptor_context().to_string() + "\n"
                                )
        except IOError as ioe:
            self.vaselogger.warning("Could not write acceptor contexts to "
                                    f"{ioe.filename}")

    # Writes the acceptor cotnexts used to construct the variant
    # contexts.
    def write_donor_context_file(self, outfileloc, samplefilter=None,
                                 contextfilter=None, chromfilter=None):
        try:
            with open(outfileloc, "w") as varcon_outfile:
                varcon_outfile.write("#ContextId\tDonorSample\tChrom\tOrigin\t"
                                     "Start\tEnd\tNumOfReads\tReadIds\n")
                for varcon in self.variant_contexts.values():
                    samplepass = self.passes_filter(
                            varcon.get_variant_context_sample(),
                            samplefilter
                            )
                    varconpass = self.passes_filter(
                            varcon.get_variant_context_id(),
                            contextfilter
                            )
                    chrompass = self.passes_filter(
                            varcon.get_variant_context_chrom(),
                            chromfilter
                            )
                    if samplepass and varconpass and chrompass:
                        varcon_outfile.write(
                            varcon.get_donor_context().to_string() + "\n"
                                )
        except IOError as ioe:
            self.vaselogger.warning("Could not write donor contexts to "
                                    f"{ioe.filename}")

    # Writes some statistics about the acceptor and donor reads
    # identified for each variant context.
    def write_variant_context_stats(self, statsoutloc):
        try:
            with open(statsoutloc, "w") as varcon_statsfile:
                varcon_statsfile.write("#ContextId\tAvg_ALen\tAvg_DLen\t"
                                       "Med_ALen\tMed_DLen\tAvg_AQual\t"
                                       "Avg_DQual\tMed_AQual\tMed_DQual\t"
                                       "Avg_AMapQ\tAvg_DMapQ\tMed_AMapQ\t"
                                       "Med_DMapQ\n")
                for varcon in self.variant_contexts.values():
                    varcon_statsfile.write(varcon.to_statistics_string() + "\n")
        except IOError as ioe:
            self.vaselogger.critical("Could not write variant context "
                                     f"statistics to {statsoutloc}")

    # Writes some statistics about the acceptor and donor reads
    # identified for each variant context.
    def write_acceptor_context_stats(self, statsoutloc):
        try:
            with open(statsoutloc, "w") as varcon_statsfile:
                varcon_statsfile.write("#ContextId\tAvg_ReadLen\tMed_ReadLen\t"
                                       "Avg_ReadQual\tMed_ReadQual\t"
                                       "Avg_ReadMapQ\tMed_ReadMapQ\n")
                for varcon in self.variant_contexts.values():
                    varcon_statsfile.write(
                            varcon.get_acceptor_context().to_statistics_string()
                            + "\n"
                            )
        except IOError as ioe:
            self.vaselogger.critical("Could not write acceptor context "
                                     f"statistics to {statsoutloc}")

    # Writes some statistics about the acceptor and donor reads
    # identified for each variant context.
    def write_donor_context_stats(self, statsoutloc):
        try:
            with open(statsoutloc, "w") as varcon_statsfile:
                varcon_statsfile.write("#ContextId\tAvg_ReadLen\tMed_ReadLen\t"
                                       "Avg_ReadQual\tMed_ReadQual\t"
                                       "Avg_ReadMapQ\tMed_ReadMapQ\n")
                for varcon in self.variant_contexts.values():
                    varcon_statsfile.write(
                            varcon.get_donor_context().to_statistics_string()
                            + "\n"
                            )
        except IOError as ioe:
            self.vaselogger.critical("Coud not write donor context statistics "
                                     f"to {statsoutloc}")

    # Writes the left and right positions to the output file.  Left pos
    # for R1 and right pos for R2.
    def write_left_right_positions(self, typetowrite, outfileloc):
        try:
            with open(outfileloc, "w") as lrpof:
                lrpof.write("#ContextId\tLeftPos\tRightPos\n")
                for varcon in self.variant_contexts.values():
                    leftpositions, rightpositions = [], []
                    if typetowrite == "acceptor":
                        leftpositions = [
                                str(x)
                                for x in varcon.get_acceptor_read_left_positions()
                                ]
                        rightpositions = [
                                str(x)
                                for x in varcon.get_acceptor_read_right_positions()
                                ]
                    if typetowrite == "donor":
                        leftpositions = [
                                str(x)
                                for x in varcon.get_donor_read_left_positions()
                                ]
                        rightpositions = [
                                str(x)
                                for x in varcon.get_donor_read_right_positions()
                                ]
                    lrpof.write(str(varcon.get_variant_context_id()) + "\t"
                                + ",".join(leftpositions) + "\t"
                                + ",".join(rightpositions))
        except IOError as ioe:
            self.vaselogger.warning("Could not write read left positions to "
                                    f"output file {outfileloc}")

    # Writes the acceptor context left and right positions to the output
    # file.  Left pos for R1 and right pos for R2.
    def write_acceptor_left_right_positions(self, outfileloc):
        try:
            with open(outfileloc, "w") as lrpof:
                lrpof.write("#ContextId\tLeftPos\tRightPos\n")
                for varcon in self.variant_contexts.values():
                    leftpositions = [
                            str(x)
                            for x in varcon.get_acceptor_context_read_left_positions()
                            ]
                    rightpositions = [
                            str(x)
                            for x in varcon.get_acceptor_context_read_right_positions()
                            ]
                    lrpof.write(str(varcon.get_variant_context_id()) + "\t"
                                + ",".join(leftpositions) + "\t"
                                + ",".join(rightpositions))
        except IOError as ioe:
            self.vaselogger.warning("Could not write read left positions to "
                                    f"output file {outfileloc}")

    # Writes the left and right positions to the output file.  Left pos
    # for R1 and right pos for R2.
    def write_donor_left_right_positions(self, outfileloc):
        try:
            with open(outfileloc, "w") as lrpof:
                lrpof.write("#ContextId\tLeftPos\tRightPos\n")
                for varcon in self.variant_contexts.values():
                    leftpositions = [
                            str(x)
                            for x in varcon.get_donor_context_read_left_positions()
                            ]
                    rightpositions = [
                            str(x)
                            for x in varcon.get_donor_context_read_right_positions()
                            ]
                    lrpof.write(str(varcon.get_variant_context_id()) + "\t"
                                + ",".join(leftpositions) + "\t"
                                + ",".join(rightpositions))
        except IOError as ioe:
            self.vaselogger.warning("Could not write read left positions to "
                                    f"output file {outfileloc}")

    # Writes the identifiers of reads that have unmapped mates per
    # sample to a file.  Samples are all donors and the ?template?.
    def write_reads_with_unmapped_mate(self, typetowrite, umfileloc):
        try:
            with open(umfileloc, "w") as umFile:
                umFile.write("#ContextId\tSampleId\tReadIds\n")
                for varcon in self.variant_contexts.values():
                    if typetowrite == "acceptor":
                        umFile.write(
                            varcon.get_variant_context_id() + "\t"
                            + str(varcon.get_variant_context_sample()) + "\t"
                            + ";".join(varcon.get_unmapped_acceptor_mate_ids())
                            )
                    if typetowrite == "donor":
                        umFile.write(
                            varcon.get_variant_context_id() + "\t"
                            + str(varcon.get_variant_context_sample()) + "\t"
                            + ";".join(varcon.get_unmapped_donor_mate_ids())
                            )
        except IOError:
            self.vaselogger.warning("Could not write read identifiers of "
                                    "reads with unmapped mates to "
                                    f"{umfileloc}")

    # Writes the unmapped mate id of the acceptor context.
    def write_acceptor_unmapped_mates(self, umfileloc):
        try:

            with open(umfileloc, "w") as umfile:
                umfile.write("#ContextId\tSampleId\tReadIds\n")
                for varcon in self.variant_contexts.values():
                    acccon = varcon.get_acceptor_context()
                    umfile.write(str(acccon.get_context_id()) + "\t"
                                 + str(acccon.get_sample_id()) + "\t"
                                 + ";".join(acccon.get_unmapped_read_mate_ids()))
        except IOError:
            self.vaselogger.warning("Could not write read identifiers of "
                                    "reads with unmapped mates to "
                                    f"{umfileloc}")

    # Writes the unmapped mate id of the donor context.
    def write_donor_unmapped_mates(self, umfileloc):
        try:
            with open(umfileloc, "w") as umFile:
                umFile.write("#ContextId\tSampleId\tReadIds\n")
                for varcon in self.variant_contexts.values():
                    doncon = varcon.get_donor_context()
                    umFile.write(str(doncon.get_context_id()) + "\t"
                                 + str(doncon.get_sample_id()) + "\t"
                                 + ";".join(doncon.get_unmapped_read_mate_ids()))
        except IOError:
            self.vaselogger.warning("Could not write read identifiers of "
                                    "reads with unmapped mates to "
                                    f"{umfileloc}")
