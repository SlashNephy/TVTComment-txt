import urllib.request
import yaml

def write_each(f, channel, value):
    if not value:
        return

    print(f"# {channel['type']}: {channel['name']}", file=f)
    if "flag" in channel:
        print("flags", channel["flag"], value, sep="\t", file=f)
    else:
        sids = []
        # GR では sid + 3 まで許容
        if channel["type"] == "GR":
            for sid in channel["serviceIds"]:
                sids.extend([sid, sid + 1, sid + 2])
        else:
            sids.extend(channel["serviceIds"])

        for sid in sids:
            print("nsid", hex(channel["networkId"] << 16 | sid), value, sep="\t", file=f)

def dump_2chthreads(data):
    with open("2chthreads.txt", "w", encoding="utf_8_sig") as f:
        print("# 2chスレ設定\n", file=f)

        print("[boards]", file=f)
        for x in data["boards"]:
            print(x["id"], x["name"], f"https://{x['server']}.5ch.net/{x['board']}/subback.html", " ".join(x.get("keywords", [])), sep="\t", file=f)

        print("\n[threadmapping]", file=f)
        for x in data["channels"]:
            for bid in x.get("boardIds", []):
                write_each(f, x, bid)

def dump_twittersearchword(data):
    with open("twittersearchword.txt", "w", encoding="utf_8_sig") as f:
        print("# Twitterリアルタイム実況の検索ワード設定\n", file=f)
        for x in data["channels"]:
            write_each(f, x, " ".join([t.lstrip("#") for t in x.get("twitterKeywords", [])]))

def dump_niconicojikkyoids(data):
    with open("niconicojikkyoids.txt", "w", encoding="utf_8_sig") as f:
        print("# ニコニコ実況の実況ID設定\n", file=f)

        for x in data["channels"]:
            write_each(f, x, x.get("nicojkId", ""))

def dump_niconicoliveids(data):
    with open("niconicoliveids.txt", "w", encoding="utf_8_sig") as f:
        print("# ニコニコ生放送の生放送ID設定\n", file=f)

        for x in data["channels"]:
            write_each(f, x, " ".join(x.get("nicoliveCommunityIds", [])))


if __name__ == "__main__":
    with urllib.request.urlopen("https://raw.githubusercontent.com/SlashNephy/saya/dev/docs/definitions.yml") as response:
        content = response.read()
        data = yaml.load(content)

    dump_2chthreads(data)
    dump_twittersearchword(data)
    dump_niconicojikkyoids(data)
    dump_niconicoliveids(data)