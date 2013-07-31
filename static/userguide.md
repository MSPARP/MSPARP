## User Guide for MSPARP

Welcome to MSPARP, a text-roleplaying chatspace on the web. At present, the website focuses on roleplaying for the popular webcomic [Homestuck](http://www.mspaintadventures.com/) by Andrew Hussie.

Here is some information to get you started…

### Selecting Your Character

Use the "> Be" dropdown to select your character. We've got (nearly) all of them. You can also use your keyboard to search for the character you want.

Once you choose a character, any information we have on that character will be filled in for you. For instance, John's Acronym will be set to <span class="egbert">EB</span> and his name will be set to <span class="egbert">ectoBiologist</span>; of course both will use his specific font color (<span class="egbert">#0715CD</span>), too!

You can modify any of these values at your leisure. Some fields provide character limits ("## left") to the right: these limit you from going too crazy with your selections.

### Control who you chat with

The new homepage makes it even easier to chat with exactly who you want. The Pester field allows you to set who you chat with, just like before. We have groups and individual characters. If you'd like to chat with every troll but <span class="nitram">Tavros</span>, set the following options:

* Pester: Trolls (Pre-Scratch), Trolls (Post-Scratch)
* Exclude: Tavros Nitram

You can place as many characters as you want in either of these fields, so go nuts customizing them to your heart's content!

##### WARNING: if you set Pester and Exclude to the same characters, or exclude groups containing all the characters you've chosen, you'll never find anyone to chat with <strike>and you'll die alone all sad and stuff</strike>.

### Typing Quirks

What good is a chat program without some options for self expression?! We have a few options set out for you:

* Typing case will alter the case of the characters you type. We offer nearly everything you could possibly want.
* Prefixes and suffixes allow you to bookend your text with a few characters.
* Letter and Pattern Replacements give you powerful tools to make your beautiful instant messages look like gibberish (see the next section).

#### Notes

* Remember that the 'lower case' option will prevent you from typing uppercase, even for proper nouns or emphasis. You may want to pick 'Normal' case and force yourself to keep your fingers off the shift keys.
* You can always 'break' out of a quirk by typing a forward slash ('/') the start of your line. If you start a line with a slash, we won't apply any quirks for you as you chat until you send that message and begin another.

### Letter & Pattern Replacement

Letter Replacements allow you to replace one or more characters with some others. For instance, as <span class="pyrope">Terezi</span> you might want to replace 'E' with '3'. You could do this by setting the left field to 'E' and one across from it to '3'. You could read it as "Replace the letter 'E' with '3'. <span class="pyrope">SW33T</span>. If you need to add or remove letter replacements, '&times;' and '+' links are available when you hover over the rows containing the letter replacement fields.

But what about characters who don't always type in uppercase? <span class="captor">Sollux</span>, for instance replaces all instances of 's' with '2', regardless of case. While we could "Replace the letter 'S' with '2'" and "Replace the letter 's' with '2'" (they're different) we have pattern replacements that can help us here. By replacing `/s/gi`, we want to globally (that's the `g`) replace all instances of the character 's' in a case insensitive (that's the `i`) manner. 

Confused? Don't fret. We're using a programming technique here called "Regular Expressions" which allow for complex pattern matching. For instance, <span class="captor">Sollux</span> has another quirk we've set up which is even more complicated: `/\b(to|too)\b/gi` will find every instance of 'to' and 'too', but not if they're part of a word. So <span class="captor">II'd love to!</span> will change to <span class="captor">II'd love two!</span> but <span class="captor">II took iit.</span> would NOT change to <span class="captor">II twok iit.</span> This type of replacement could never be done without using regular expressions. 

To learn regular expressions, talk to the nerdiest person you know, or use these resources:

* [W3 Schools JS RegExp Object Reference](http://www.w3schools.com/jsref/jsref_obj_regexp.asp)
* [Regular-Expressions.info](http://www.regular-expressions.info/index.html) - Learn Regular Expressions
* http://www.regex101.com/ - test regular expressions in the browser

Rest assured that we've set a bunch of these up for you :)

### All Those Buttons

We're introducing something called Personas for you all. Personas allow you to create settings for a character and save them for later, then load them in at will. You can even share them with friends by copying and pasting information.

#### Save

Once you've got your character just right, the Save button allows you to Save the persona for later. If you've never done this before, you'll be prompted to choose a name. If you've got personas saved already, you'll be able to save over your existing personas which will replace the settings for that persona with these new settings.

#### Load

Once you've saved a persona, Load will be available. If it's not available to you, you have no saved personas in this browser. Load allows you to choose one of those personas and get chatting or customize it further. Remember that if you customize a persona once you load it into the homepage, you'll need to save it for those changes to persist for the next time you visit the site.

#### Manage

The manage screen allows you to do three things:

* Rename personas to change their names
* Delete individual personas to keep things fresh, and
* Delete all personas.

Renaming personas is easy. Choose one from the list, then type a new name and save: you're done.

Deleting individual personas is easy, too. Choose one from the list and the '&times;' icon to the right will remove it from the system for you. You'll be given a confirmation dialog before this is final.

Deleting all personas is a big deal, so when you tap the big red Clear button, you'll get a pretty intense message reminding you that you can't undo this action. If you wanna go through with it, just type "DELETE" (all caps, no quotes) in the field as you're instructed to and choose Okay. Bye bye, personas!

#### Import / Export

You set up all these great personas but you lost your mind and did it in Internet Explorer. How are you ever going to get them out? You can use the Import / Export feature to do this. In IE, click Import / Export and copy the block of text that appears in the modal window. Once done, you can click the same button in Chrome, Firefox, Safari or anything else and paste it in.

"But Ms. Parp," you say arrogantly… "What if I have two personas with the same name? You're not gonna clobber one of my dear, sweet personas, are you?" No, Ms. Parp is a pacifist. She'll append " (Imported --------------)" to the one you import. Those dashes will be replaced with a big number to make sure you don't run into any collisions when importing your data. You can then go and rename personas or delete them in the Manage dialog (see above).

### Group Chat

To start your own group chat, you just need to pick a URL and go for it. URLs are formatted like so: `http://www.msparp.com/chat/a-string-of-letters-and-numbers-here` and instead of writing `a-string-of-letters-and-numbers-here`, you would just put a string of letters and numbers, without spaces.

For example, your group chat could be called `http://www.msparp.com/chat/penguin` or `http://www.msparp.com/chat/icannotfindthepumpkin413`

### I'm lost!

If you are still having trouble, boy do you have options! You can hit up our [forums](http://msparp-forums.org/) to ask for help. You can drop by our [Tumblr](http://msparp.tumblr.com/) and drop us an [ask](http://msparp.tumblr.com/ask), or you can… just keep trying to figure it out? If you're really nice, maybe you can get us on speaker crab and we'll help you out verbally.
