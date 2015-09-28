# Introduction #

You may use these rules to prepare your library for the handling by Library Organizer.

Thanks a lot to 600WPMPO for sharing these!

# The Rules #

```
# sample configuration provided by 600WMPO
## rules for cr Data Man
#rules to prepare for LibraryOrganizer (MainCharacterOrTeam) 
# 
#DC Comics 
<<Series.Contains:Animal Man>> <<Publisher:DC Comics>> => <<MainCharacterOrTeam:Animal Man>> 
<<Series.Contains:Aquaman>> <<Publisher:DC Comics>> => <<MainCharacterOrTeam:Aquaman>> 
<<Series.Contains:Blue Beetle>> <<Publisher:DC Comics>> => <<MainCharacterOrTeam:Blue Beetle>> 
<<Series.Contains:Firestorm>> <<Publisher:DC Comics>> => <<MainCharacterOrTeam:Firestorm>> 
<<Series.Contains:Flash>> <<Publisher:DC Comics>> => <<MainCharacterOrTeam:Flash>> 
<<Series.Contains:Green Arrow>> <<Publisher:DC Comics>> => <<MainCharacterOrTeam:Green Arrow>> 
<<Series:Arrow>> <<Publisher:DC Comics>> => <<MainCharacterOrTeam:Green Arrow>> 
<<Series.Contains:Hawkman>> <<Publisher:DC Comics>> => <<MainCharacterOrTeam:Hawkman>> 
<<Series.Contains:Swamp Thing>> <<Publisher:DC Comics>> => <<MainCharacterOrTeam:Swamp Thing>> 
<<Series.Contains:Wonder Woman>> <<Publisher:DC Comics>> => <<MainCharacterOrTeam:Wonder Woman>> 
# 
#Marvel 
<<Series.Contains:Avengers>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Avengers>> 
<<Series.Contains:Captain America>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Captain America>> 
<<Series.Contains:Daredevil>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Daredevil>> 
<<Series.Contains:Deadpool>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Deadpool>> 
<<Series.Contains:Fantastic Four>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Fantastic Four>> 
<<Series:FF>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Fantastic Four>> 
<<Series.Contains:Ghost Rider>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Ghost Rider>> 
<<Series.Contains:Hulk>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Hulk>> 
<<Series.Contains:Iron Man>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Iron Man>> 
<<Series.Contains:Nova>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Nova>> 
<<Series.Contains:Punisher>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Punisher>> 
<<Series.Contains:Punisher>> <<Publisher:Max>> => <<MainCharacterOrTeam:Punisher>> 
<<Series.Contains:Scarlet Spider>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Spider-Man>> 
<<Series.Contains:Spider-Girl>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Spider-Man>> 
<<Series.Contains:Spider-Man>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Spider-Man>> 
<<Series.Contains:Spider-Men>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Spider-Man>> 
<<Series.Contains:Journey Into Mystery>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Thor>> 
<<Series.Contains:Thor>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Thor>> 
<<Series.Contains:Venom>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Spider-Man>> 
<<Series.Contains:Winter Soldier>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Captain America>> 
<<Series.Contains:Wolverine>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:Wolverine>> 
<<Series.Contains:X-Men>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:X-Men>> 
<<Series.Contains:X-Force>> <<Publisher:Marvel>> => <<MainCharacterOrTeam:X-Force>> 
# 
#Indie 
<<Series.Contains:Conan>> <<Publisher:Dark Horse Comics>> => <<MainCharacterOrTeam:Conan>> 
<<Series.Contains:Vampirella>> <<Publisher:Dynamite Entertainment>> => <<MainCharacterOrTeam:Vampirella>> 
<<Series.Contains:The Darkness>> <<Publisher:Top Cow>> => <<MainCharacterOrTeam:The Darkness>> 
<<Series.Contains:Witchblade>> <<Publisher:Top Cow>> => <<MainCharacterOrTeam:Witchblade>> 
<<Series.Contains:Doctor Who>> <<Publisher:IDW Publishing>> => <<MainCharacterOrTeam:Doctor Who>> 
<<Series.Contains:Angel>> <<Publisher:IDW Publishing>> => <<MainCharacterOrTeam:Angel>> 
<<Series.Contains:Spawn>> <<Publisher:Image>> => <<MainCharacterOrTeam:Spawn>> 
<<Series.Contains:Hellspawn>> <<Publisher:Image>> => <<MainCharacterOrTeam:Spawn>> 
<<Series.StartsWith:Green Hornet>> <<Publisher:Dynamite Entertainment>> => <<MainCharacterOrTeam:Green Hornet>> 
<<Series.StartsWith:The Green Hornet>> <<Publisher:Dynamite Entertainment>> => <<MainCharacterOrTeam:Green Hornet>> 
<<Series.StartsWith:Kato>> <<Publisher:Dynamite Entertainment>> => <<MainCharacterOrTeam:Green Hornet>> 
<<Series.Contains:G.I. Joe>> <<Publisher:IDW Publishing>> => <<MainCharacterOrTeam:G.I. Joe>> 
# 
#rules to prepare for LibraryOrganizer (SeriesGroup) 
#DC Comics 
<<Series.Contains:Batman>> <<Publisher:DC Comics>> => <<SeriesGroup:Gotham City>> 
<<Series.Contains:Gotham>> <<Publisher:DC Comics>> => <<SeriesGroup:Gotham City>> 
<<Series.Contains:Nightwing>> <<Publisher:DC Comics>> => <<SeriesGroup:Gotham City>> 
<<Series.Contains:Batwoman>> <<Publisher:DC Comics>> => <<SeriesGroup:Gotham City>> 
<<Series.Contains:Detective Comics>> <<Publisher:DC Comics>> => <<SeriesGroup:Gotham City>> 
<<Series.Contains:Birds of prey>> <<Publisher:DC Comics>> => <<SeriesGroup:Gotham City>> 
<<Series.Contains:Batwing>> <<Publisher:DC Comics>> => <<SeriesGroup:Gotham City>> 
<<Series.Contains:Batgirl>> <<Publisher:DC Comics>> => <<SeriesGroup:Gotham City>> 
<<Series.Contains:Catwoman>> <<Publisher:DC Comics>> => <<SeriesGroup:Gotham City>> 
<<Series.Contains:Justice League>> <<Publisher:DC Comics>> => <<SeriesGroup:Justice League>> 
<<Series.Contains:Superman>> <<Publisher:DC Comics>> => <<SeriesGroup:Metropolis>> 
<<Series.Contains:Superboy>> <<Publisher:DC Comics>> => <<SeriesGroup:Metropolis>> 
<<Series.Contains:Supergirl>> <<Publisher:DC Comics>> => <<SeriesGroup:Metropolis>> 
<<Series.Contains:Power Girl>> <<Publisher:DC Comics>> => <<SeriesGroup:Metropolis>> 
<<Series.Contains:Adventure Comics>> <<Publisher:DC Comics>> => <<SeriesGroup:Metropolis>> 
<<Series.Contains:Action Comics>> <<Publisher:DC Comics>> => <<SeriesGroup:Metropolis>> 
<<Series.Contains:Krypton>> <<Publisher:DC Comics>> => <<SeriesGroup:Metropolis>> 
<<Series.Contains:Green Lantern>> <<Publisher:DC Comics>> => <<SeriesGroup:OA>> 
<<Series.Contains:Red Lantern>> <<Publisher:DC Comics>> => <<SeriesGroup:OA>> 
<<Series.Contains:Emerald Warriors>> <<Publisher:DC Comics>> => <<SeriesGroup:OA>> 
# 
#Marvel 
<<Series.Contains:Ultimate>> <<Publisher:Marvel>> => <<SeriesGroup:Ultimate>> 
# 
#Indie 
<<Series.Contains:Star Wars>> <<Publisher:Dark Horse Comics>> => <<SeriesGroup:Star Wars>> 
<<Series.Contains:Hellboy>> <<Publisher:Dark Horse Comics>> => <<SeriesGroup:Hellboy>> 
<<Series.Contains:Lobster Johnson>> <<Publisher:Dark Horse Comics>> => <<SeriesGroup:Hellboy>> 
<<Series.Contains:Abe Sapien>> <<Publisher:Dark Horse Comics>> => <<SeriesGroup:Hellboy>> 
<<Series.Contains:B.P.R.D.>> <<Publisher:Dark Horse Comics>> => <<SeriesGroup:Hellboy>> 
<<Series.Contains:B.P.R.D>> <<Publisher:Dark Horse Comics>> => <<SeriesGroup:Hellboy>> 
<<Series.Contains:BPRD>> <<Publisher:Dark Horse Comics>> => <<SeriesGroup:Hellboy>> 
# 
#rules to prepare for LibraryOrganizer (Format) 
<<Series.Contains:Annual>> => <<Format:Annual>> 
<<FileDirectory.Contains:Annual>> => <<Format:Annual>> 
<<Series.StartsWith:Age of Ultron>> => <<Format:Crossover>> 
<<FilePath.Contains:Annual>> => <<Format:Annual>> 
# 
#rules to prepare for LibraryOrganizer (Count) 
<<Format:>> <<Count.Greater:0>> <<Publisher:Marvel>> => <<Format:Limited Series>> 
<<Format:>> <<Count.Greater:0>> <<Publisher:DC Comics>> => <<Format:Limited Series>> 
<<Format:>> <<Count.Greater:0>> <<Publisher.Not:Marvel>> <<MainCharacterOrTeam.Not:>> => <<Format:Limited Series>> 
<<Format:>> <<Count.Greater:0>> <<Publisher.Not:DC Comics>> <<MainCharacterOrTeam.Not:>> => <<Format:Limited Series>> 
<<Format:>> <<Count.Less:1>> <<Publisher:Marvel>> => <<Format:Main Series>> 
<<Format:>> <<Count.Less:1>> <<Publisher:DC Comics>> => <<Format:Main Series>> 
<<Format:>> <<Count.Less:1>> <<Publisher.Not:Marvel>> <<MainCharacterOrTeam.Not:>> => <<Format:Main Series>> 
<<Format:>> <<Count.Less:1>> <<Publisher.Not:DC Comics>> <<MainCharacterOrTeam.Not:>> => <<Format:Main Series>>


```