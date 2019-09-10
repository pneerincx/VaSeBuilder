import statistics
from OverlapContext import OverlapContext


class VariantContext:
    """Saves a variant context and allows data to be obtained and calculated.

    Attributes
    ----------
    context_id : str
        Identifier of the context
    sample_id : str
        The name/identifier of the donor sample used to construct the variant context
    variant_context_chrom : str
        Chromosome name the context is lcoated on
    variant_context_origin : int
        Variant position the context is constructed from
    variant_context_start : int
        Leftmost genomic position of the variant context
    variant_context_end : int
        Rightmost genomic position of the variant context
    variant_context_areads : list of DonorBamRead
        Acceptor reads associated with the variant context
    variant_context_dreads : list of DonorBamRead
        Donor reads associated with the variant context
    variant_acceptor_context : OverlapContext
        Acceptor context used to construct the variant context
    variant_donor_context : OverlapContext
        Donor context used to construct the variant context
    unmapped_donor_mate_ids : list of str
        Identifiers of reads with an unmapped mate
    """

    # Sets the variant context data.
    def __init__(self, varconid, sampleid,
                 varconchrom, varconorigin,
                 varconstart, varconend,
                 acceptorreads, donorreads,
                 acceptor_context=None, donor_context=None):
        """Saves the provided variant context data.

        Acceptor and donor contexts are optional when creating the variant context.

        Parameters
        ----------
        varconid : str
            Variant context identifier
        sampleid : str
            Sample name/identifier
        varconchrom : str
            Chromosome name the variant context is located on
        varconorigin:
            Variant position the context is constructed from
        varconstart : int
            Leftmost genomic position of the variant context
        varconend : int
            Rightmost genomic position of the variant context
        acceptorreads : list of DonorBamRead
            Variant context acceptor reads
        donorreads : list of DonorBamRead
            Variant context donor reads
        acceptor_context : OverlapContext
            Acceptor context associated with the variant context
        donor_context : OverlapContext
            Donor context associated with the variant context
        """
        self.context_id = varconid
        self.sample_id = sampleid
        self.variant_context_chrom = varconchrom
        self.variant_context_origin = int(varconorigin)
        self.variant_context_start = int(varconstart)
        self.variant_context_end = int(varconend)
        # Saves the acceptor reads that overlap with the entire variant context.
        self.variant_context_areads = acceptorreads
        # Saves the donor reads that overlap with the entire variant context.
        self.variant_context_dreads = donorreads
        # Saves the acceptor context (this is the context from acceptor reads overlapping with the variant itself).
        self.variant_acceptor_context = acceptor_context
        # Saves the donor context (this is the context from donor reads overlapping with the variant itself).
        self.variant_donor_context = donor_context
        self.unmapped_acceptor_mate_ids = []
        self.unmapped_donor_mate_ids = []

    # ===METHODS TO OBTAIN DATA FROM THE VARIANT CONTEXT DATA==================
    def get_variant_context_id(self):
        """Returns the variant context identifier.

        Returns
        -------
        self.context_id : str
            Variant context identifier
        """
        return self.context_id

    def get_variant_context_sample(self):
        """Returns the name/identifier of the sample

        Returns
        -------
        self.sample_id : str
            Sample name/identifier
        """
        return self.sample_id

    def get_variant_context_chrom(self):
        """Returns the chromosome name the variant context is located on.

        Returns
        -------
        self.variant_context_chrom : str
            Chromosome name of the variant context
        """
        return self.variant_context_chrom

    def get_variant_context_origin(self):
        """Returns the genomic position of the variant used to construct the variant context.

        Returns
        -------
        self.variant_context_origin : int
            Variant genomic position
        """
        return self.variant_context_origin

    def get_variant_context_start(self):
        """Returns the leftmost genomic position of the variant context.

        Returns
        -------
        self.variant_context_start
            Variant context starting position
        """
        return self.variant_context_start

    def get_variant_context_end(self):
        """Returns the variant context end position.

        Returns
        -------
        self.variant_context_end : int
            Variant context rightmost genomic position
        """
        return self.variant_context_end

    def get_acceptor_reads(self):
        """Returns the variant context acceptor reads.

        Returns
        -------
        self.variant_context_areads : list of DonorBamRead
            Variant context acceptor reads
        """
        return self.variant_context_areads

    # Returns the variant context donor reads.
    def get_donor_reads(self):
        """Returns the variant context donor reads.

        Returns
        -------
        self.variant_context_dreads : list of DonorBamRead
            Variant context acceptor reads
        """
        return self.variant_context_dreads

    # TODO: New thing for -P mode.
    def get_donor_read_strings(self):
        donorreads = []
        for dbr in self.variant_context_dreads:
            donorreads.append((dbr.get_bam_read_id(),
                              dbr.get_bam_read_pair_number(),
                              dbr.get_bam_read_sequence(),
                              dbr.get_bam_read_qual()))
        return list(set(donorreads))

    def get_acceptor_context(self):
        """Returns the acceptor context used to construct the variant context.

        Returns
        -------
        self.variant_acceptor_context : OverlapContext
            Acceptor context associated with the variant context
        """
        return self.variant_acceptor_context

    # Returns the donor context (the context from donor reads overlapping the variant itself).
    def get_donor_context(self):
        """Returns the donor context used to construct the variant context.

        Returns
        -------
        self.variant_donor_context : OverlapContext
            Donor context associated with the variant context
        """
        return self.variant_donor_context

    # Returns a list of acceptor reads overlapping with the variant context.
    def get_unmapped_acceptor_mate_ids(self):
        return self.unmapped_acceptor_mate_ids

    # Returns a list of donor reads overlapping with the variant context.
    def get_unmapped_donor_mate_ids(self):
        return self.unmapped_donor_mate_ids

    # ===METHODS TO GET DATA (REQUIRING SOME CALCULATING) OF THE VARIANT CONTEXT===============
    def get_variant_context_length(self):
        """Returns the length of the variant context.

        The length if determined by subtracting the leftmost genomic (start) position from the rightmost genomic (end)
        position.

        Returns
        -------
        int
            Variant context length
        """
        return abs(self.variant_context_end - self.variant_context_start)

    def get_start_distance_from_origin(self):
        """Calculates and returns the variant context start from the variant position that constructed it.

        Returns
        -------
        int
            Distance between variant context leftmost genomic and variant position.
        """
        return abs(self.variant_context_origin - self.variant_context_start)

    def get_end_distance_from_origin(self):
        """Calculates and returns the variant context end from the variant position tha constructed it.

        Returns
        -------
        int
            Distance between variant context rightmost genomic and variant position
        """
        return abs(self.variant_context_end - self.variant_context_origin)

    # ===METHODS TO OBTAIN VARIANT CONTEXT ACCEPTOR READ DATA==================
    def get_number_of_acceptor_reads(self):
        """Returns the number of variant context acceptor reads.

        Returns
        -------
        int
            Number of variant context acceptor reads
        """
        if self.variant_context_areads is None:
            return 0
        return len(self.variant_context_areads)

    def get_acceptor_read_ids(self):
        """Returns the variant context acceptor read identifiers

        Returns
        -------
        list of str or None
            Variant context acceptor read identifiers, None if there are no acceptor reads
        """
        if self.variant_context_areads is None:
            return [None]
        return list(set([x.get_bam_read_id() for x in self.variant_context_areads]))

    def get_acceptor_read_starts(self):
        """Returns the variant context acceptor read starting positions

        Returns
        -------
        list of int or None
            Variant context acceptor read leftmost genomic positions, None if there are no acceptor reads
        """
        if self.variant_context_areads is None:
            return [None]
        return [x.get_bam_read_ref_pos() for x in self.variant_context_areads]

    def get_acceptor_read_left_positions(self):
        """Returns the leftmost genomic positions of all variant context R1 acceptor reads.

        Returns
        -------
        list of int or None
            Variant context R1 acceptor read leftmost genomic positions, None of there are no acceptor reads
        """
        if self.variant_context_areads is None:
            return [None]
        return [x.get_bam_read_ref_pos()
                for x in self.variant_context_areads if x.is_read1()]

    def get_acceptor_read_ends(self):
        """Returns the variant context acceptor read rightmost positions.

        Returns
        -------
        list of int or None
            Variant context R2 acceptor read rightmost genomic positions, None if there are no acceptor reads
        """
        if self.variant_context_areads is None:
            return [None]
        return [x.get_bam_read_ref_end() for x in self.variant_context_areads]

    def get_acceptor_read_right_positions(self):
        """Returns the rightmost genomic positions for all variant context R2 acceptor reads

        Returns
        -------
        list of int or None
            Variant context
        """
        if self.variant_context_areads is None:
            return [None]
        return [x.get_bam_read_ref_end()
                for x in self.variant_context_areads if x.is_read2()]

    # ===METHODS TO OBTAIN VARIANT CONTEXT DONOR READ DATA=====================
    def get_number_of_donor_reads(self):
        """Returns the number of variant context donor reads.

        Returns
        -------
        int
            Number of variant context donor reads
        """
        return len(self.variant_context_dreads)

    def get_donor_read_ids(self):
        """Returns the identifiers of donor reads overlapping with the variant context.

        Returns
        -------
        list of str
            Variant context donor read identifiers
        """
        return list(set([x.get_bam_read_id() for x in self.variant_context_dreads]))

    def get_donor_read_starts(self):
        """Returns the list of variant context donor read starting positions.

        Returns
        -------
        list of int
            Variant context donor read leftmost genomic positions
        """
        return [x.get_bam_read_ref_pos() for x in self.variant_context_dreads]

    def get_donor_read_left_positions(self):
        """Returns the list of variant context R1 donor read leftmost positions

        Returns
        -------
        list of int
            Variant context R1 donor read leftmost genomic positions
        """
        return [x.get_bam_read_ref_pos()
                for x in self.variant_context_dreads if (x.is_read1())]

    # Returns a list of all donor read ending positions
    def get_donor_read_ends(self):
        """Returns variant context donor read rightmost positions.

        Returns
        -------
        list of int
            Variant context donor read rightmost genomic positions
        """
        return [x.get_bam_read_ref_end() for x in self.variant_context_dreads]

    def get_donor_read_right_positions(self):
        """Returns the list of variant context R2 donor reads 

        Returns
        -------
        list of int
            Variant context R2 donor reads rightmost genomic positions
        """
        return [x.get_bam_read_ref_end()
                for x in self.variant_context_dreads if (x.is_read2())]

    # ===METHODS TO ADD DATA TO THE VARIANT CONTEXT============================
    def set_acceptor_context(self, acceptor_context):
        """Sets the acceptor context of the variant context with the one provided.

        Parameters
        ----------
        acceptor_context : OverlapContext
            Acceptor context to add to the variant context
        """
        self.variant_acceptor_context = acceptor_context

    def set_donor_context(self, donor_context):
        """Sets the donor context of the variant context with the one provided.

        Parameters
        ----------
        donor_context : OverlapContext
            Donor context to add to the variant context
        """
        self.variant_donor_context = donor_context

    def add_acceptor_context(self, contextid, sampleid,
                             contextchrom, contextorigin,
                             contextstart, contextend,
                             acceptorreads):
        """Sets the acceptor context of the variant context by constructing one from the provided parameters.

        Parameters
        ----------
        contextid : str
            Acceptor context identifier
        sampleid : str
            Sample name/identifier
        contextchrom : str
            Chromosome name the context is located on
        contextorigin : int
            Variant position the context is constructed from
        contextstart : int
            Leftmost genomic position of the acceptor context
        contextend : int
            Rightmost genomic position of the acceptor context
        acceptorreads : list of DonorBamRead
            Acceptor context reads
        """
        self.variant_acceptor_context = OverlapContext(
                contextid, sampleid,
                contextchrom, contextorigin,
                contextstart, contextend,
                acceptorreads
                )

    def add_donor_context(self, contextid, sampleid,
                          contextchrom, contextorigin,
                          contextstart, contextend,
                          donorreads):
        """Sets the donor context of the variant context by constructing one from the provided parameters.

        Parameters
        ----------
        contextid : str
            Donor context identifier
        sampleid : str
            Sample name/identifier
        contextchrom : str
            Chromosome name the context is located on
        contextorigin : int
            Variant genomic position the context is constructed from
        contextstart : int
            Leftmost genomic position of the donor context
        contextend : int
            Rightmost genomic position of the donor context
        donorreads : list of DonorBamRead
            Donor context reads
        """
        self.variant_donor_context = OverlapContext(
                contextid, sampleid,
                contextchrom, contextorigin,
                contextstart, contextend,
                donorreads
                )

    # ===METHODS TO OBTAIN VARIANT CONTEXT UNMAPPED MATE READ DATA=============
    def get_unmapped_acceptor_read_ids(self):
        """Returns the variant context acceptor read identifiers that have an unmapped mate.

        Returns
        -------
        self.unmapped_acceptor_mate_ids : list of str
            Variant context acceptor read identifiers with an unmapped mate
        """
        return self.unmapped_acceptor_mate_ids

    def get_unmapped_donor_read_ids(self):
        """Returns the variant context donor read identifiers that have an unmapped mate.

        Returns
        -------
        self.unmapped_donor_mate_ids : list of str
            Variant context donor read identifiers with an unmapped mate
        :return:
        """
        return self.unmapped_donor_mate_ids

    def add_unmapped_acceptor_mate_id(self, mateid):
        """Adds a variant context appector mate identifier.

        Parameters
        ----------
        mateid : str
            Variant context acceptor read identifier with an unmapped mate
        """
        self.unmapped_acceptor_mate_ids.append(mateid)

    def add_unmapped_donor_mate_id(self, mateid):
        """Adds a variant context donor mate identifier.

        Parameters
        ----------
        mateid : str
            Variant context donor read identifier with an unmapped mate
        """
        self.unmapped_donor_mate_ids.append(mateid)

    def set_unmapped_acceptor_mate_ids(self, mateids):
        """Sets the variant context unmapped acceptor mate ids.

        Parameters
        ----------
        mateids : list of str
            Variant context acceptor read identifiers with unmapped mate
        """
        self.unmapped_acceptor_mate_ids = mateids

    def set_unmapped_donor_mate_ids(self, mateids):
        """Sets the variant context unmapped donor mate ids.

        Parameters
        ----------
        mateids : list of str
            Variant context donor read identifiers with unmapped mates
        """
        self.unmapped_donor_mate_ids = mateids

    def acceptor_read_has_unmapped_mate(self, readid):
        """Returns whether a specified variant context acceptor read has an unmapped mate.

        Parameters
        ----------
        readid : str
            Acceptor read identifier

        Returns
        -------
        bool
            True if acceptor read has unmapped mate, False if not
        """
        return readid in self.unmapped_acceptor_mate_ids

    def donor_read_has_unmapped_mate(self, readid):
        """Checks and returns whether a specified variant context donor read has an unmapped mate.

        Parameters
        ----------
        readid : str
            Donor read identifier

        Returns
        -------
        bool
            True if donor read has unmapped mate, False if not
        """
        return readid in self.unmapped_donor_mate_ids

    def get_number_of_unmapped_acceptor_mates(self):
        """Returns the number of variant context acceptor reads with an unmapped mate.

        Returns
        -------
        int
            Number of variant context acceptor reads with an unmapped mate.
        """
        return len(self.unmapped_acceptor_mate_ids)

    def get_number_of_unmapped_donor_mates(self):
        """Returns the number of variant context donor reads with an unmapped mate.

        Returns
        -------
        int
            Number of variant context donor reads with an unmapped mate.
        """
        return len(self.unmapped_donor_mate_ids)

    # ===METHODS TO ADD UNMAPPED MATES TO THE ACCEPTOR AND DONOR CONTEXT=======
    def set_acceptor_context_unmapped_mates(self, mateids):
        """Sets the unmapped mate ids for the acceptor context.

        Returns
        -------
        mateids : list of str
            Acceptor context read identifiers with an unmapped mate
        """
        self.variant_acceptor_context.set_unmapped_mate_ids(mateids)

    def add_acceptor_context_unmapped_mate(self, ureadid):
        """Adds an unmapped read id to the acceptor context.

        Parameters
        ----------
        ureadid : str
            Acceptor context read identifier with an unmapped mate
        """
        self.variant_acceptor_context.add_unmapped_mate_id(ureadid)

    def set_donor_context_unmapped_mates(self, mateids):
        """Sets the unmapped mate ids for the donor context.

        Parameters
        ----------
        mateids : list of str
            Donor context read identifiers with an unmapped mate
        """
        self.variant_donor_context.set_unmapped_mate_ids(mateids)

    def add_donor_context_unmapped_mate(self, ureadid):
        """Adds an unmapped read id to the donor context.

        Parameters
        ----------
        ureadid : str
            Donor context read identifier with an unmapped mate
        """
        self.variant_donor_context.add_unmapped_mate_id(ureadid)

    # ===METHODS TO OBTAIN STATISTICS OF THE VARIANT CONTEXT===================
    def get_average_and_median_acceptor_read_qual(self):
        """Returns the average and median quality of the acceptor reads associated with.

        Returns
        -------

        """
        return self.get_average_and_median_read_qual(self.variant_context_areads)

    def get_average_and_median_donor_read_qual(self):
        """Calculates and returns the mean and median variant context donor read Q-Score.

        Returns
        -------
        list of int
            Mean and median Q-Score
        """
        return self.get_average_and_median_read_qual(self.variant_context_dreads)

    def get_average_and_median_read_qual(self, contextreads):
        """Calculates and returns the mean and median read Q-Score.

        Parameters
        ----------
        contextreads : list or reads
            Reads to calculate mean and median Q-Score of

        Returns
        -------
        """
        if contextreads is not None:
            avgmedqual = []
            for contextread in contextreads:
                avgmedqual.append(contextread.get_average_qscore())
            return ([statistics.mean(avgmedqual),
                     statistics.median(avgmedqual)])
        return [None, None]

    def get_average_and_median_acceptor_read_mapq(self):
        """Calculates and returns the mean and median variant context acceptor read MAPQ value.

        Returns
        -------
        list of int
            Mean and median MAPQ, None if there are no acceptor reads
        """
        return self.get_average_and_median_read_mapq(self.variant_context_areads)

    def get_average_and_median_donor_read_mapq(self):
        """Calculates and returns the mean and median variant context donor read MAPQ value.

        Returns
        -------
        list of int
            Mean and median variant context donor read MAPQ, None if there are no donor reads
        """
        return self.get_average_and_median_read_mapq(self.variant_context_dreads)

    def get_average_and_median_read_mapq(self, contextreads):
        """Calculates and returns the mean and median MAPQ value of provided reads.

        Parameters
        ----------
        contextreads : list of DonorBamRead
            Reads to calculate mean and median MAPQ of

        Returns
        -------
        list of int
            Mean and median read MAPQ, None if no reads provided
        """
        if contextreads is not None:
            avgmedmapq = []
            for contextread in contextreads:
                avgmedmapq.append(contextread.get_mapping_qual())
            return ([statistics.mean(avgmedmapq),
                     statistics.median(avgmedmapq)])
        return [None, None]

    def get_average_and_median_acceptor_read_length(self):
        """Calculates and returns the mean and median variant context acceptor read length.

        Returns
        -------
        list of int
            Mean and median variant context acceptor read length, None if there are no acceptor reads
        """
        return self.get_average_and_median_read_length(self.variant_context_areads)

    def get_average_and_median_donor_read_length(self):
        """Calculates and returns the mean and median variant context donor read length.

        Returns
        -------
        list of int
            Mean and median variant context donor read length, None if there are no donor reads
        """
        return self.get_average_and_median_read_length(self.variant_context_dreads)

    def get_average_and_median_read_length(self, contextreads):
        """Calculates and returns the mean and median read length of a specified list of reads.

        Parameters
        ----------
        contextreads : list of DonorBamReds
            Reads to to calculate mean and median length of

        Returns
        -------
        list of int
            Mean and median read length, None if no reads are supplied
        """
        if contextreads is not None:
            avgmedlen = []
            for contextread in contextreads:
                if contextread.get_bam_read_length() is not None:
                    avgmedlen.append(contextread.get_bam_read_length())
            return [statistics.mean(avgmedlen), statistics.median(avgmedlen)]
        return [None, None]

    # ===METHODS TO OBTAIN ACCEPTOR CONTEXT DATA===============================
    def has_acceptor_context(self):
        """Returns whether the variant context has an acceptor context

        Returns
        -------
        bool
            True if variant context has an acceptor context, False if not
        """
        return self.variant_acceptor_context is not None

    def get_acceptor_context_id(self):
        """Returns the acceptor context identifier.

        Returns
        -------
        str
            Acceptor context identifier
        """
        return self.variant_acceptor_context.get_context_id()

    def get_acceptor_context_sample_id(self):
        """Returns the acceptor context sample id.

        Returns
        -------
        str
            Sample name/identifier of the acceptor context
        """
        return self.variant_acceptor_context.get_sample_id()

    def get_acceptor_context_chrom(self):
        """Returns the chromosome name of the acceptor context.

        Returns
        -------
        str
            Chromosome name the acceptor context is located on
        """
        return self.variant_acceptor_context.get_context_chrom()

    def get_acceptor_context_origin(self):
        """Returns the origin position of the acceptor context.

        Returns
        -------
        int
            Variant genomic position the context is based on
        """
        return self.variant_acceptor_context.get_context_origin()

    def get_acceptor_context_start(self):
        """Returns the starting position of the acceptor context.

        Returns
        -------
        int
            Acceptor context leftmost genomic position
        """
        return self.variant_acceptor_context.get_context_start()

    def get_acceptor_context_end(self):
        """Returns the ending position of the acceptor context.

        Returns
        -------
        int
            Acceptor context rightmost genomic position
        """
        return self.variant_acceptor_context.get_context_end()

    def get_acceptor_context_length(self):
        """Returns the length of the acceptor context.

        Returns
        -------
        int
            Acceptor context length
        """
        return self.variant_acceptor_context.get_context_length()

    def get_acceptor_context_reads(self):
        """Returns the acceptor context reads.

        Returns
        -------
        list of DonorBamRead
            Acceptor context reads
        """
        return self.variant_acceptor_context.get_context_bam_reads()

    def get_acceptor_context_read_ids(self):
        """Returns the acceptor context read identifiers.

        Returns
        -------
        list of str
            Acceptor context read identifiers
        """
        return self.variant_acceptor_context.get_context_bam_read_ids()

    def get_acceptor_context_read_starts(self):
        """Returns the leftmost genomic positions of the acceptor context reads

        Returns
        -------
        """
        return self.variant_acceptor_context.get_context_bam_read_starts()

    def get_acceptor_context_read_left_positions(self):
        """Returns the leftmost genomic positions of all R1 acceptor context reads

        Returns
        -------
        list of int
            Acceptor context leftmost genomic R1 read positions
        """
        return self.variant_acceptor_context.get_context_bam_read_left_positions()

    def get_acceptor_context_read_ends(self):
        """Returns the rightmost genomic positions of all acceptor context reads.

        Returns
        -------
        list of int
            Acceptor context rightmost genomic read positions.
        """
        return self.variant_acceptor_context.get_context_bam_read_ends()

    def get_acceptor_context_read_right_positions(self):
        """Returns a list of all acceptor context R2 BAM read end positions.

        Returns
        -------
        list of int
            Acceptor context rightmost genomic R2 read positions
        """
        return self.variant_acceptor_context.get_context_bam_read_right_positions()

    def get_acceptor_context_read_lengths(self):
        """Returns the lengths of the acceptor context reads.

        Returns
        -------
        list of int
            Acceptor context read lengths
        """
        return self.variant_acceptor_context.get_context_bam_read_lengths()

    def get_acceptor_context_unmapped_mate_ids(self):
        """Returns the acceptor context read identifiers with unmapped mates.

        Returns
        -------
        list of str
            Acceptor context read identifiers with unmapped mates.
        """
        return self.variant_acceptor_context.get_unmapped_read_mate_ids()

    # ===METHODS TO OBTAIN DONOR CONTEXT DATA==================================
    def has_donor_context(self):
        """Checks and returns whether the variant context has a donor context saved.

        Returns
        -------
        bool
            True if the variant context has a donor context, False if not
        """
        return self.variant_donor_context is not None

    def get_donor_context_id(self):
        """Returns the donor context identifier.

        Returns
        -------
        str
            Donor context identifier
        """
        return self.variant_donor_context.get_context_id()

    def get_donor_context_sample_id(self):
        """Returns the sample name/identifier of the donor context

        Returns
        -------
        str
            Donor context sample name/identifier
        """
        return self.variant_donor_context.get_sample_id()

    def get_donor_context_chrom(self):
        """Returns the chromosome of the donor context.

        Returns
        -------
        """
        return self.variant_donor_context.get_context_chrom()

    def get_donor_context_origin(self):
        """Returns the origin position of the donor context.
        
        Returns
        -------
        int
            Variant genomic position that the context is constructed from.
        """
        return self.variant_donor_context.get_context_origin()

    def get_donor_context_start(self):
        """Returns the starting position of the donor context.

        Returns
        -------
        int
            Donor context leftmost genomic position
        """
        return self.variant_donor_context.get_context_start()

    def get_donor_context_end(self):
        """Returns the ending position of the donor context.

        Returns
        -------
        int
            Donor context rightmost genomic position
        """
        return self.variant_donor_context.get_context_end()

    def get_donor_context_length(self):
        """Returns the length of the donor context.

        Returns
        -------
        int
            Donor context length
        """
        return self.variant_donor_context.get_context_length()

    def get_donor_context_reads(self):
        """Returns all donor context reads.

        Returns
        -------
        list of DonorBamRead
            Donor context reads
        """
        return self.variant_donor_context.get_context_bam_reads()

    def get_donor_context_read_ids(self):
        """Returns the identifiers of all donor context reads.

        Returns
        -------
        list of str
            Donor context read identifiers
        """
        return self.variant_donor_context.get_context_bam_read_ids()

    def get_donor_context_read_starts(self):
        """Returns the leftmost genomic read positions of all donor context reads.

        Returns
        -------
        list of int
            Donor context leftmost genomic read positions
        """
        return self.variant_donor_context.get_context_bam_read_starts()

    def get_donor_context_read_left_positions(self):
        """Returns the leftmost genomic positions of all R1 donor context reads.

        Returns
        -------
        list of int
            Donor context leftmost genomic R1 read positions
        """
        return self.variant_donor_context.get_context_bam_read_left_positions()

    def get_donor_context_read_ends(self):
        """Returns the rightmost genomic positions of all donor context reads.

        Returns
        -------
        list of int
            Donor context rightmost genomic read positions
        """
        return self.variant_donor_context.get_context_bam_read_ends()

    def get_donor_context_read_right_positions(self):
        """Returns the rightmost genomic positions of all R2 donor context reads

        Returns
        -------
        list of int
            Donor context rightmost genomic R2 read positions
        """
        return self.variant_donor_context.get_context_bam_read_right_positions()

    def get_donor_context_read_lengths(self):
        """Returns the lengths of the donor context reads.

        Returns
        -------
        list of int
            Donor context read lengths
        """
        return self.variant_donor_context.get_context_bam_read_lengths()

    def get_donor_context_unmapped_mate_ids(self):
        """Returns the donor context read identifiers that have unmapped mates.

        Returns
        -------
        list of str
            Donor context read identifiers
        """
        return self.variant_donor_context.get_unmapped_read_mate_ids()

    # ===METHODS TO PRODUCE SOME OUTPUT ABOUT THE VARIANT CONTEXT==============
    def to_string(self):
        """Creates and returns the variant context as a String representation.

        The created String representation of the variant context is equal to the entry of a variant context file. Each
        included data attribute is separated by a tab.

        Returns
        -------
        str
            Variant context as variant context file entry
        """
        if self.variant_context_areads is None:
            ad_ratio = "N/A"
            list_areads = None
            acon_len = None
            aread_count = 0
        else:
            ad_ratio = float(len(self.variant_context_areads)
                             / len(self.variant_context_dreads))
            areads = list(set(self.get_acceptor_read_ids()))
            areads.sort()
            list_areads = ";".join(areads)
            acon_len = self.variant_acceptor_context.get_context_length()
            aread_count = len(self.variant_context_areads)
        dreads = list(set(self.get_donor_read_ids()))
        dreads.sort()
        list_dreads = ";".join(dreads)
        return (str(self.context_id) + "\t"
                + str(self.sample_id) + "\t"
                + str(self.variant_context_chrom) + "\t"
                + str(self.variant_context_origin) + "\t"
                + str(self.variant_context_start) + "\t"
                + str(self.variant_context_end) + "\t"
                + str(acon_len) + "\t"
                + str(self.variant_donor_context.get_context_length()) + "\t"
                + str(aread_count) + "\t"
                + str(len(self.variant_context_dreads)) + "\t"
                + str(ad_ratio) + "\t"
                + str(list_areads) + "\t"
                + str(list_dreads))

    # Returns a varconstats.txt string representation of the variant context.
    def to_statistics_string(self):
        """Returns a String with basic variant context statistics.

        Returns
        -------
        str
            Basic tab separated variant context statistics
        """
        areadlen = self.get_average_and_median_acceptor_read_length()
        dreadlen = self.get_average_and_median_donor_read_length()
        areadqual = self.get_average_and_median_acceptor_read_qual()
        dreadqual = self.get_average_and_median_donor_read_qual()
        areadmapq = self.get_average_and_median_acceptor_read_mapq()
        dreadmapq = self.get_average_and_median_donor_read_mapq()
        return (str(self.context_id) + "\t"
                + str(areadlen[0]) + "\t"
                + str(dreadlen[0]) + "\t"
                + str(areadlen[1]) + "\t"
                + str(dreadlen[1]) + "\t"
                + str(areadqual[0]) + "\t"
                + str(dreadqual[0]) + "\t"
                + str(areadqual[1]) + "\t"
                + str(dreadqual[1]) + "\t"
                + str(areadmapq[0]) + "\t"
                + str(dreadmapq[0]) + "\t"
                + str(areadmapq[1]) + "\t"
                + str(dreadmapq[1]))
