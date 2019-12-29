# Approach 1

def flatten(d, sep="_", r_obj="JSON"):
    import collections

    obj = dict() if r_obj == "JSON" else collections.OrderedDict()

    def recurse(t, parent_key=""):

        if isinstance(t, list):
            for i in range(len(t)):
                recurse(t[i], parent_key + sep + str(i) if parent_key else str(i))
        elif isinstance(t, dict):
            for k, v in t.items():
                recurse(v, parent_key + sep + k if parent_key else k)
        else:
            obj[parent_key] = t

    recurse(d)

    return obj


# Approach 2
def flatten_json(y):
    out = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + "_")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


if __name__ == "__main__":
  data = {
      "id": 1,
      "first_name": "Ronnie",
      "last_name": "Joshua",
      "employment_history": [
          {
              "company": "PyR Analytica",
              "title": "Data Analyst",
              "Complex Object": {"hello": [1, 2, 3, {"something": "goes"}]},
          },
          {"Previous Org": "PyR Analytica", "title": "Data Engineer"},
      ],
      "education": {
          "bachelors": "Mathematical Economics",
          "masters": "Economics & Computer Science",
          "phd": "Higher Education",
      },
  }


  flatten(data)
  flatten_json(data)
