# GoSports

<!-- Contributors: Sam DeFrancisco, Kyle Rooney, Shannon McCarty, Kaya Zdan 

Django Models Overview:
![gosports](https://user-images.githubusercontent.com/72476187/165991399-1858bf07-b722-4874-bd98-4a7a87503d5f.png)
-->

<div id="top"></div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#screen-shots">Screen Shots</a></li>
  </ol>
</details>


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]






<!-- ABOUT THE PROJECT -->
## About The Project

Gosports is a full Stack Django web app that displays historical/live Nba Statistics. This project was created by me and three other students from Iowa State University (See Contact) in a 8 week time-span, broke into four two week sprints.
The app was built in a private instance of GitLab for Iowa State University, hence no commit history. After submitting the project I decided to upload it to my personal GitHub.

### Features
* View live scores of games going on today
* See current NBA standings
* Look at your favorite teams roster, as well as each players indivual stats that season
* View each active nba players career, also see common info about that player (height, weight, position, jersey #)
* See the upcoming schedule (current week)
* Create Account
<p align="left">(<a href="#screen-shots">See Screenshots</a>)</p>



### Built With
* [Django](https://www.djangoproject.com/)
* [Python](https://www.python.org/)
* [sqlite3](https://www.sqlite.org/index.html)
* HTML & CSS
<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Sam DeFrancisco - sjdefran@gmail.com

GM: Kyle Rooney, Kaya Zdan, Shannon McCarty

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
Nba Api is what allowed this entire project to come together with real information. They have information for getting started making basic calls to their API within their github.

* [nba_api](https://github.com/swar/nba_api)
* [w3 Schools HTML & CSS Tutorials](https://www.webpagefx.com/tools/emoji-cheat-sheet)

<p align="right">(<a href="#top">back to top</a>)</p>

## Screen Shots


### Team and Player Pages
#### Choose Team Page
![choose_team](https://user-images.githubusercontent.com/72476187/166098756-b93696a3-f131-4b0f-9713-0bd15258a68d.png)

#### Specific Player Page (1)
![tatum_overview](https://user-images.githubusercontent.com/72476187/166098772-d1f6ca81-fed1-484e-9f38-7ec698039806.png)
#### Career view (2)
![tatum_career](https://user-images.githubusercontent.com/72476187/166098795-5088c34b-9b5c-4069-9563-d6a46f9f0a38.png)

### Home Page
#### Live Scores and Game times available using game_standings.py
![image](https://user-images.githubusercontent.com/72476187/166098813-0b0570ae-b509-444f-88e6-70cb7ce98da8.png)

### Standings
![image](https://user-images.githubusercontent.com/72476187/166098735-c741b513-5889-4b28-8ed3-4c0c37f51383.png)
### Schedule
![schedule](https://user-images.githubusercontent.com/72476187/165996625-673a78f5-d38b-41d9-b4bc-87411451a7cc.png)

#### Team Page
#### (1)
![specific_team1](https://user-images.githubusercontent.com/72476187/165996792-174a3fa0-e116-4911-8868-afb747c2480b.png)
#### (2)
![specific_team2](https://user-images.githubusercontent.com/72476187/165996863-fb20872a-4beb-412f-98b5-093fe0addb21.png)

### Search Functionality
#### Teams
![team_search](https://user-images.githubusercontent.com/72476187/166099835-5a3c651d-3f99-423c-a0f3-563e704b4139.png)
#### Players
![player_search](https://user-images.githubusercontent.com/72476187/166099866-d9587209-40e1-4ada-9593-2917bcfdfc59.png)

### Django Models Design:
![gosports_db](https://user-images.githubusercontent.com/72476187/165996178-c3003bbe-5e9f-43fe-a276-a144997c8926.png)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/sam-defrancisco-4373361b3/
