function addOrReplace(org, key, value) {
  if (org.endsWith("#")) {
    org = org.substring(0, org.length - 1)
  }
  var stringToAdd = key + "=" + value;
  // First query param
  if (org.indexOf("?") == -1)
    return org + "?" + stringToAdd;

  if (org.indexOf(key + "=") == -1)
    return org + "&" + stringToAdd;

  var searchParams = org.split("?")[1].split("&");
  for (var i = 0; i < searchParams.length; i++) {
    if (searchParams[i].indexOf(key + "=") > -1) {
      searchParams[i] = key + "=" + value;
      break;
    }
  }
  return org.split("?")[0] + "?" + searchParams.join("&");
}
