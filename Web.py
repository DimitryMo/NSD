{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.7.4"
    },
    "colab": {
      "name": "Web.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "toc_visible": true,
      "include_colab_link": true
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/DimitryMo/NSD/blob/master/Web.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "LEVn_EVIkaiK",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "from bs4 import BeautifulSoup\n",
        "import requests\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "import re"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "FK-4sG79kaiy",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def cleanhtml(raw_html):\n",
        "  cleanr = re.compile('<.*?>')\n",
        "  cleantext = re.sub(cleanr, '', raw_html)\n",
        "  regex = re.compile('[^A-Za-zА-Яа-я]')\n",
        "  cleantext = regex.sub(' ', cleantext)\n",
        "  return cleantext"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "CC025IC2kai7",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "\n",
        "def document(id):\n",
        "    page = requests.get('https://vc.ru/trade/' + str(id) )\n",
        "    soup = BeautifulSoup(page.text, 'html5lib')\n",
        "    info = []\n",
        "    if soup.find(\"h1\", class_=\"content-header__title\"):\n",
        "        #titledone\n",
        "        info.append(soup.find(\"h1\", class_=\"content-header__title\").text.split())\n",
        "        #text не знаю как решить, почему-то выдает заглавие и раздел, \n",
        "        #хотя у них другой класс\n",
        "        text = soup.find(\"div\", class_=\"layout--a\").text\n",
        "        info.append(cleanhtml(text).split())\n",
        "        #yeardone\n",
        "        info.append(soup.find(\"time\", class_= \"time\").text.split()[2])\n",
        "        #sectiondone\n",
        "        info.append(soup.find(\"div\", class_=\n",
        "                              \"content-header-author__name\").text.split())\n",
        "        #votesdone\n",
        "        info.append(soup.find(\"span\", class_=\n",
        "                              \"vote__value__v vote__value__v--real\").text)\n",
        "        #viewsdone\n",
        "        info.append(soup.find(\"span\", class_=\"views__value\").text)\n",
        "        #bookmarksdone\n",
        "        a = soup.find(\"span\", class_=\"vote__value__v vote__value__v--real\").text\n",
        "        if a[0] == '–':\n",
        "            b = int(a[1:])\n",
        "            info.append(-b)\n",
        "        else:\n",
        "            info.append(int(a))\n",
        "        #commentsdone\n",
        "        comment1 = soup.find_all(\"div\", class_=\"comments__item__text\")\n",
        "        comments = []\n",
        "        for i in range(len(comment1)):\n",
        "            comments.append(comment1[i].text)\n",
        "        info.append(comments)\n",
        "    else:\n",
        "        info.append('NaN')\n",
        "    print(id)\n",
        "    return info\n",
        "    "
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "anhcVb_6kajA",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "a = list(map(document, np.arange(#начало, #конец)))\n"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "2K4pFE7zkajG",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "df = pd.DataFrame(a, columns=['title', 'text', 'year', 'section', 'votes', 'views', 'bookmarks', 'comments'])\n",
        "df.dropna(inplace=True)\n",
        "print(df)"
      ],
      "execution_count": 0,
      "outputs": []
    }
  ]
}