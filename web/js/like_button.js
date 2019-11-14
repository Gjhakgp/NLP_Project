'use strict';
// import { React.styled-components;
const e = React.createElement;
const parent_url=""
class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: true,files:[],file_data:[],loader:false };
  }
  helper(data){
    let temp=[]
    let temp1=[]
    console.log(data)
    data.forEach(elem=>{
      var regex = /\d+/g;
      var matches = elem.match(regex);
      let bn=parseInt(matches[0])
      // console.log("assss",bn)
      temp.push(bn)
    })
    // temp.sort()
    temp.sort(function(a, b){
      return a - b;
    });
    console.log(temp);
    temp.forEach(elem=>{
      let kn="file"+elem.toString()+".xml"
      // console.log(kn)
      temp1.push(kn)
    })
    this.setState({files:temp1})
  }
  async componentDidMount(){
    // const response=await fetch(parent_url+"get/files?lang=en&tag=all")
    // const data=await response.json()
    let data=await fetch(parent_url+"get/files?lang=en&tag=all").then(response=>response.json()).then(json=>this.helper(json))
  }
  async handleClick(e){
    this.setState({loader:true})
    console.log(e);
    await fetch(parent_url+"get/data?filename="+e).then(response=>response.json()).then(json=>this.setState({file_data:json}))
    this.setState({loader:false});
  }
  getsidenav(){
    let f=this.state.files;
    let ret=[]
    if(f.length==0){
      return(<p></p>)
    }else{
     ret=f.map(el=>(<div><button class="btn btn-primary mb-1" onClick={() => this.handleClick(el)}>{el}</button></div>))
     return ret;
  }
}
getmainbody(){
  let f=this.state.file_data;
  let stylecontent="card-header m-2 border border-primary overflow-auto w-auto"
  var st3={minWidth: "150px",maxWidth: "150px",maxHeight: "1000px",boxSizing:"inherit",overflow:"scroll"}
  let ret=[]
  if(f.length==0){
    return(<p></p>)
  }else{
    ret.push(<h1>{f["event_type"][0]}</h1>)
    ret.push(<div class={stylecontent}>{f["content"]}</div>)
    let temp1=f["args"]["CASUALTIES-ARG"]
    let str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div  class={stylecontent}>{"CASUALTIES-arg"}<p>{str1}</p></div>)
    temp1=f["args"]["PLACE-ARG"]
    str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div class={stylecontent}>{"PLACE-arg"}<p>{str1}</p></div>)
    temp1=f["args"]["TIME-ARG"]
    str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div class={stylecontent}>{"TIME-arg"}<p>{str1}</p></div>)

    try {
      temp1=f["args"]["REASON-ARG"]
      str1="";
      temp1.forEach(element => {
        str1=str1+","+element;
      });
      ret.push(<div class={stylecontent}>{"REASON-arg"}<p>{str1}</p></div>)
    } catch (error) {
      
    }
    try {
      temp1=f["args"]["PARTICIPANT-ARG"]
      str1="";
      temp1.forEach(element => {
        str1=str1+","+element;
      });
      ret.push(<div class={stylecontent}>{"PARTICIPANT-arg"}<p>{str1}</p></div>)
    } catch (error) {
      
    }
    temp1=f["model_data"]["what"]
    str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div class={stylecontent}>{"what-arg"}<p>{str1}</p></div>)

    temp1=f["model_data"]["when"]
    str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div class={stylecontent}>{"when-arg"}<p>{str1}</p></div>)

    temp1=f["model_data"]["where"]
    str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div class={stylecontent}>{"where-arg"}<p>{str1}</p></div>)

    temp1=f["model_data"]["who"]
    str1="";
    temp1.forEach(element => {
      str1=str1+","+element;
    });
    ret.push(<div class={stylecontent}>{"who-arg"}<p>{str1}</p></div>)

    temp1=f["model_data"]["why"]
    str1="";
    temp1.forEach(element => {
      str1=str1+element+",";
    });
    ret.push(<div class={stylecontent}>{"why-arg"}<p>{str1}</p></div>)
    let ret1=ret.map(e=><div class="card">{e}</div>)
    return ret1;
  }
}
  render() {
    // console.log(this.state.files)
    let sidenavx=this.getsidenav()
    let mainbody1=this.getmainbody()
    var st2={maxHeight: "768px",boxSizing:"inherit"}
    var st3={minWidth: "150px",maxWidth: "150px",maxHeight: "1000px",boxSizing:"inherit",overflow:"scroll"}
    let st6;
    if(this.state.loader){
      let temp1x=[<div id="sidenav1" class="col-sm" style={st3}>{sidenavx}</div>,<img style={st6} class="col-md" src="https://i.giphy.com/media/xTk9ZvMnbIiIew7IpW/giphy.webp" alt="loader"/>]
      let temp2x=[<div class="row">{temp1x.map(elem=>elem)}</div>];
      return( 
        <div id="inReact" class="container m-0" style={st2}>
        {temp2x.map(elem=>elem)}
      </div>
       )
    }
    let temp1=[<div id="sidenav1" class="col-sm" style={st3}>{sidenavx}</div>,<div id="mainbody" style={st6} class="col-md">{mainbody1}</div>]
    let temp=[<div class="row">{temp1.map(elem=>elem)}</div>];
    // var st2={maxHeight: "768px",boxSizing:"inherit"}
    return(
      <div id="inReact" class="container m-0" style={st2}>
        {temp.map(elem=>elem)}
      </div>
    )
  }
}

ReactDOM.render(<App/>,document.getElementById('root'));

