# Minting the DOI

Four steps, none of which anyone but the repository owner can do, because each
needs the owner's Zenodo account.

1. Sign in at <https://zenodo.org> with GitHub.
2. Go to <https://zenodo.org/account/settings/github/> and switch this
   repository **on**. Zenodo then watches it for releases.
3. Cut a release here (`gh release create <tag> --verify-tag`, or the web UI).
   Zenodo archives that tag and mints a DOI within a minute or two.

   **The order matters.** Zenodo picks up releases made *after* the repository
   is switched on; a release cut before step 2 is not archived and gets no DOI,
   and the tag name is then used up. So do not cut the release early. (Zenodo's
   own documentation does not state this outright, which is why it is worth
   saying: their GitHub guide assumes throughout that the repository is already
   enabled.)
4. Two DOIs appear: a **concept DOI** that always resolves to the newest
   version, and a **version DOI** fixed to this release. Put the concept DOI in
   the paper — it is the one that stays right when the archive is updated.

`.zenodo.json` in this repository is already filled in, so the deposit's title,
author, licence, keywords and description are populated automatically; nothing
has to be typed into the web form.

## Then, in the paper

Replace `[ARCHIVAL DOI TO BE SUPPLIED]` in the *Code and data* section with the
concept DOI. The commit hash named beside it stays: a DOI pins a snapshot, and
the hash says which snapshot the numbers came from.

## A caution learned here

This repository's tag was moved twice while the archive was being assembled, and
each time something that pointed at it pointed at the wrong thing. Zenodo
archives whatever the tag names at the moment the release is cut. Cut the
release from a commit you do not intend to touch again, and do not move the tag
afterwards.
