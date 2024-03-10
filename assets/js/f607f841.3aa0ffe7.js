"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1620],{4418:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>u,contentTitle:()=>l,default:()=>m,frontMatter:()=>i,metadata:()=>c,toc:()=>d});var r=n(85893),a=n(11151),o=n(74866),s=n(85162);const i={},l="Getting Started",c={id:"Getting-Started",title:"Getting Started",description:"AutoGen is a framework that enables development of LLM applications using",source:"@site/docs/Getting-Started.mdx",sourceDirName:".",slug:"/Getting-Started",permalink:"/autogen/docs/Getting-Started",draft:!1,unlisted:!1,editUrl:"https://github.com/microsoft/autogen/edit/main/website/docs/Getting-Started.mdx",tags:[],version:"current",frontMatter:{},sidebar:"docsSidebar",next:{title:"Introduction to AutoGen",permalink:"/autogen/docs/tutorial/introduction"}},u={},d=[{value:"Main Features",id:"main-features",level:3},{value:"Quickstart",id:"quickstart",level:3},{value:"Multi-Agent Conversation Framework",id:"multi-agent-conversation-framework",level:4},{value:"Where to Go Next?",id:"where-to-go-next",level:3}];function h(e){const t={a:"a",admonition:"admonition",code:"code",h1:"h1",h3:"h3",h4:"h4",img:"img",li:"li",p:"p",pre:"pre",ul:"ul",...(0,a.a)(),...e.components};return(0,r.jsxs)(r.Fragment,{children:[(0,r.jsx)(t.h1,{id:"getting-started",children:"Getting Started"}),"\n",(0,r.jsx)(t.p,{children:"AutoGen is a framework that enables development of LLM applications using\nmultiple agents that can converse with each other to solve tasks. AutoGen agents\nare customizable, conversable, and seamlessly allow human participation. They\ncan operate in various modes that employ combinations of LLMs, human inputs, and\ntools."}),"\n",(0,r.jsx)(t.p,{children:(0,r.jsx)(t.img,{alt:"AutoGen Overview",src:n(25515).Z+"",width:"1576",height:"756"})}),"\n",(0,r.jsx)(t.h3,{id:"main-features",children:"Main Features"}),"\n",(0,r.jsxs)(t.ul,{children:["\n",(0,r.jsxs)(t.li,{children:["AutoGen enables building next-gen LLM applications based on ",(0,r.jsx)(t.a,{href:"/docs/Use-Cases/agent_chat",children:"multi-agent\nconversations"})," with minimal effort. It simplifies\nthe orchestration, automation, and optimization of a complex LLM workflow. It\nmaximizes the performance of LLM models and overcomes their weaknesses."]}),"\n",(0,r.jsxs)(t.li,{children:["It supports ",(0,r.jsx)(t.a,{href:"/docs/Use-Cases/agent_chat#supporting-diverse-conversation-patterns",children:"diverse conversation\npatterns"}),"\nfor complex workflows. With customizable and conversable agents, developers can\nuse AutoGen to build a wide range of conversation patterns concerning\nconversation autonomy, the number of agents, and agent conversation topology."]}),"\n",(0,r.jsxs)(t.li,{children:["It provides a collection of working systems with different complexities. These\nsystems span a ",(0,r.jsx)(t.a,{href:"/docs/Use-Cases/agent_chat#diverse-applications-implemented-with-autogen",children:"wide range of\napplications"}),"\nfrom various domains and complexities. This demonstrates how AutoGen can\neasily support diverse conversation patterns."]}),"\n"]}),"\n",(0,r.jsxs)(t.p,{children:["AutoGen is powered by collaborative ",(0,r.jsx)(t.a,{href:"/docs/Research",children:"research studies"})," from\nMicrosoft, Penn State University, and University of Washington."]}),"\n",(0,r.jsx)(t.h3,{id:"quickstart",children:"Quickstart"}),"\n",(0,r.jsx)(t.pre,{children:(0,r.jsx)(t.code,{className:"language-sh",children:"pip install pyautogen\n"})}),"\n",(0,r.jsxs)(o.Z,{children:[(0,r.jsxs)(s.Z,{value:"local",label:"Local execution",default:!0,children:[(0,r.jsx)(t.admonition,{type:"warning",children:(0,r.jsx)(t.p,{children:"When asked, be sure to check the generated code before continuing to ensure it is safe to run."})}),(0,r.jsx)(t.pre,{children:(0,r.jsx)(t.code,{className:"language-python",children:'from autogen import AssistantAgent, UserProxyAgent\nfrom autogen.coding import LocalCommandLineCodeExecutor\n\nimport os\nfrom pathlib import Path\n\nllm_config = {\n    "config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}],\n}\n\nwork_dir = Path("coding")\nwork_dir.mkdir(exist_ok=True)\n\nassistant = AssistantAgent("assistant", llm_config=llm_config)\n\ncode_executor = LocalCommandLineCodeExecutor(work_dir=work_dir)\nuser_proxy = UserProxyAgent(\n    "user_proxy", code_execution_config={"executor": code_executor}\n)\n\n# Start the chat\nuser_proxy.initiate_chat(\n    assistant,\n    message="Plot a chart of NVDA and TESLA stock price change YTD.",\n)\n'})})]}),(0,r.jsxs)(s.Z,{value:"docker",label:"Docker execution",default:!0,children:[(0,r.jsx)(t.pre,{children:(0,r.jsx)(t.code,{className:"language-python",children:'from autogen import AssistantAgent, UserProxyAgent\nfrom autogen.coding import DockerCommandLineCodeExecutor\n\nimport os\nfrom pathlib import Path\n\nllm_config = {\n    "config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}],\n}\n\nwork_dir = Path("coding")\nwork_dir.mkdir(exist_ok=True)\n\nwith DockerCommandLineCodeExecutor(work_dir=work_dir) as code_executor:\n    assistant = AssistantAgent("assistant", llm_config=llm_config)\n    user_proxy = UserProxyAgent(\n        "user_proxy", code_execution_config={"executor": code_executor}\n    )\n\n    # Start the chat\n    user_proxy.initiate_chat(\n        assistant,\n        message="Plot a chart of NVDA and TESLA stock price change YTD. Save the plot to a file called plot.png",\n    )\n'})}),(0,r.jsxs)(t.p,{children:["Open ",(0,r.jsx)(t.code,{children:"coding/plot.png"})," to see the generated plot."]})]})]}),"\n",(0,r.jsx)(t.admonition,{type:"tip",children:(0,r.jsxs)(t.p,{children:["Learn more about configuring LLMs for agents ",(0,r.jsx)(t.a,{href:"/docs/topics/llm_configuration",children:"here"}),"."]})}),"\n",(0,r.jsx)(t.h4,{id:"multi-agent-conversation-framework",children:"Multi-Agent Conversation Framework"}),"\n",(0,r.jsxs)(t.p,{children:["Autogen enables the next-gen LLM applications with a generic multi-agent conversation framework. It offers customizable and conversable agents which integrate LLMs, tools, and humans.\nBy automating chat among multiple capable agents, one can easily make them collectively perform tasks autonomously or with human feedback, including tasks that require using tools via code. For ",(0,r.jsx)(t.a,{href:"https://github.com/microsoft/autogen/blob/main/test/twoagent.py",children:"example"}),","]}),"\n",(0,r.jsx)(t.p,{children:"The figure below shows an example conversation flow with AutoGen."}),"\n",(0,r.jsx)(t.p,{children:(0,r.jsx)(t.img,{alt:"Agent Chat Example",src:n(81890).Z+"",width:"2188",height:"1200"})}),"\n",(0,r.jsx)(t.h3,{id:"where-to-go-next",children:"Where to Go Next?"}),"\n",(0,r.jsxs)(t.ul,{children:["\n",(0,r.jsxs)(t.li,{children:["Go through the ",(0,r.jsx)(t.a,{href:"/docs/tutorial/introduction",children:"tutorial"})," to learn more about the core concepts in AutoGen"]}),"\n",(0,r.jsxs)(t.li,{children:["Read the examples and guides in the ",(0,r.jsx)(t.a,{href:"/docs/notebooks",children:"notebooks section"})]}),"\n",(0,r.jsxs)(t.li,{children:["Understand the use cases for ",(0,r.jsx)(t.a,{href:"/docs/Use-Cases/agent_chat",children:"multi-agent conversation"})," and ",(0,r.jsx)(t.a,{href:"/docs/Use-Cases/enhanced_inference",children:"enhanced LLM inference"})]}),"\n",(0,r.jsxs)(t.li,{children:["Read the ",(0,r.jsx)(t.a,{href:"/docs/reference/agentchat/conversable_agent/",children:"API"})," docs"]}),"\n",(0,r.jsxs)(t.li,{children:["Learn about ",(0,r.jsx)(t.a,{href:"/docs/Research",children:"research"})," around AutoGen"]}),"\n",(0,r.jsxs)(t.li,{children:["Chat on ",(0,r.jsx)(t.a,{href:"https://discord.gg/pAbnFJrkgZ",children:"Discord"})]}),"\n",(0,r.jsxs)(t.li,{children:["Follow on ",(0,r.jsx)(t.a,{href:"https://twitter.com/pyautogen",children:"Twitter"})]}),"\n"]}),"\n",(0,r.jsxs)(t.p,{children:["If you like our project, please give it a ",(0,r.jsx)(t.a,{href:"https://github.com/microsoft/autogen/stargazers",children:"star"})," on GitHub. If you are interested in contributing, please read ",(0,r.jsx)(t.a,{href:"/docs/Contribute",children:"Contributor's Guide"}),"."]}),"\n",(0,r.jsx)("iframe",{src:"https://ghbtns.com/github-btn.html?user=microsoft&repo=autogen&type=star&count=true&size=large",frameborder:"0",scrolling:"0",width:"170",height:"30",title:"GitHub"})]})}function m(e={}){const{wrapper:t}={...(0,a.a)(),...e.components};return t?(0,r.jsx)(t,{...e,children:(0,r.jsx)(h,{...e})}):h(e)}},85162:(e,t,n)=>{n.d(t,{Z:()=>s});n(67294);var r=n(36905);const a={tabItem:"tabItem_Ymn6"};var o=n(85893);function s(e){let{children:t,hidden:n,className:s}=e;return(0,o.jsx)("div",{role:"tabpanel",className:(0,r.Z)(a.tabItem,s),hidden:n,children:t})}},74866:(e,t,n)=>{n.d(t,{Z:()=>k});var r=n(67294),a=n(36905),o=n(12466),s=n(16550),i=n(20469),l=n(91980),c=n(67392),u=n(50012);function d(e){return r.Children.toArray(e).filter((e=>"\n"!==e)).map((e=>{if(!e||(0,r.isValidElement)(e)&&function(e){const{props:t}=e;return!!t&&"object"==typeof t&&"value"in t}(e))return e;throw new Error(`Docusaurus error: Bad <Tabs> child <${"string"==typeof e.type?e.type:e.type.name}>: all children of the <Tabs> component should be <TabItem>, and every <TabItem> should have a unique "value" prop.`)}))?.filter(Boolean)??[]}function h(e){const{values:t,children:n}=e;return(0,r.useMemo)((()=>{const e=t??function(e){return d(e).map((e=>{let{props:{value:t,label:n,attributes:r,default:a}}=e;return{value:t,label:n,attributes:r,default:a}}))}(n);return function(e){const t=(0,c.l)(e,((e,t)=>e.value===t.value));if(t.length>0)throw new Error(`Docusaurus error: Duplicate values "${t.map((e=>e.value)).join(", ")}" found in <Tabs>. Every value needs to be unique.`)}(e),e}),[t,n])}function m(e){let{value:t,tabValues:n}=e;return n.some((e=>e.value===t))}function p(e){let{queryString:t=!1,groupId:n}=e;const a=(0,s.k6)(),o=function(e){let{queryString:t=!1,groupId:n}=e;if("string"==typeof t)return t;if(!1===t)return null;if(!0===t&&!n)throw new Error('Docusaurus error: The <Tabs> component groupId prop is required if queryString=true, because this value is used as the search param name. You can also provide an explicit value such as queryString="my-search-param".');return n??null}({queryString:t,groupId:n});return[(0,l._X)(o),(0,r.useCallback)((e=>{if(!o)return;const t=new URLSearchParams(a.location.search);t.set(o,e),a.replace({...a.location,search:t.toString()})}),[o,a])]}function g(e){const{defaultValue:t,queryString:n=!1,groupId:a}=e,o=h(e),[s,l]=(0,r.useState)((()=>function(e){let{defaultValue:t,tabValues:n}=e;if(0===n.length)throw new Error("Docusaurus error: the <Tabs> component requires at least one <TabItem> children component");if(t){if(!m({value:t,tabValues:n}))throw new Error(`Docusaurus error: The <Tabs> has a defaultValue "${t}" but none of its children has the corresponding value. Available values are: ${n.map((e=>e.value)).join(", ")}. If you intend to show no default tab, use defaultValue={null} instead.`);return t}const r=n.find((e=>e.default))??n[0];if(!r)throw new Error("Unexpected error: 0 tabValues");return r.value}({defaultValue:t,tabValues:o}))),[c,d]=p({queryString:n,groupId:a}),[g,f]=function(e){let{groupId:t}=e;const n=function(e){return e?`docusaurus.tab.${e}`:null}(t),[a,o]=(0,u.Nk)(n);return[a,(0,r.useCallback)((e=>{n&&o.set(e)}),[n,o])]}({groupId:a}),x=(()=>{const e=c??g;return m({value:e,tabValues:o})?e:null})();(0,i.Z)((()=>{x&&l(x)}),[x]);return{selectedValue:s,selectValue:(0,r.useCallback)((e=>{if(!m({value:e,tabValues:o}))throw new Error(`Can't select invalid tab value=${e}`);l(e),d(e),f(e)}),[d,f,o]),tabValues:o}}var f=n(72389);const x={tabList:"tabList__CuJ",tabItem:"tabItem_LNqP"};var b=n(85893);function v(e){let{className:t,block:n,selectedValue:r,selectValue:s,tabValues:i}=e;const l=[],{blockElementScrollPositionUntilNextRender:c}=(0,o.o5)(),u=e=>{const t=e.currentTarget,n=l.indexOf(t),a=i[n].value;a!==r&&(c(t),s(a))},d=e=>{let t=null;switch(e.key){case"Enter":u(e);break;case"ArrowRight":{const n=l.indexOf(e.currentTarget)+1;t=l[n]??l[0];break}case"ArrowLeft":{const n=l.indexOf(e.currentTarget)-1;t=l[n]??l[l.length-1];break}}t?.focus()};return(0,b.jsx)("ul",{role:"tablist","aria-orientation":"horizontal",className:(0,a.Z)("tabs",{"tabs--block":n},t),children:i.map((e=>{let{value:t,label:n,attributes:o}=e;return(0,b.jsx)("li",{role:"tab",tabIndex:r===t?0:-1,"aria-selected":r===t,ref:e=>l.push(e),onKeyDown:d,onClick:u,...o,className:(0,a.Z)("tabs__item",x.tabItem,o?.className,{"tabs__item--active":r===t}),children:n??t},t)}))})}function w(e){let{lazy:t,children:n,selectedValue:a}=e;const o=(Array.isArray(n)?n:[n]).filter(Boolean);if(t){const e=o.find((e=>e.props.value===a));return e?(0,r.cloneElement)(e,{className:"margin-top--md"}):null}return(0,b.jsx)("div",{className:"margin-top--md",children:o.map(((e,t)=>(0,r.cloneElement)(e,{key:t,hidden:e.props.value!==a})))})}function j(e){const t=g(e);return(0,b.jsxs)("div",{className:(0,a.Z)("tabs-container",x.tabList),children:[(0,b.jsx)(v,{...e,...t}),(0,b.jsx)(w,{...e,...t})]})}function k(e){const t=(0,f.Z)();return(0,b.jsx)(j,{...e,children:d(e.children)},String(t))}},25515:(e,t,n)=>{n.d(t,{Z:()=>r});const r=n.p+"assets/images/autogen_agentchat-250ca64b77b87e70d34766a080bf6ba8.png"},81890:(e,t,n)=>{n.d(t,{Z:()=>r});const r=n.p+"assets/images/chat_example-da70a7420ebc817ef9826fa4b1e80951.png"},11151:(e,t,n)=>{n.d(t,{Z:()=>i,a:()=>s});var r=n(67294);const a={},o=r.createContext(a);function s(e){const t=r.useContext(o);return r.useMemo((function(){return"function"==typeof e?e(t):{...t,...e}}),[t,e])}function i(e){let t;return t=e.disableParentContext?"function"==typeof e.components?e.components(a):e.components||a:s(e.components),r.createElement(o.Provider,{value:t},e.children)}}}]);