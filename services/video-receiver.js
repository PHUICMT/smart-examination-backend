const fs = require("fs");

const VideoReceiver = (data) => {
  let fileName = data["fileName"];
  let blob = data.data;
  let type = data.type;

  // console.log(fileName);
  // console.log(data);

  // let file = new File(blob, fileName, {
  //   type: type,
  //   lastModified: new Date().getTime(),
  // });

  // fs.createWriteStream("../videos" + fileName).write(blob);
};

module.exports = { VideoReceiver };
