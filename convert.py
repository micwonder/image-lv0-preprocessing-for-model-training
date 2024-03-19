(function () {
  const iav = {};

  const scriptTag =
    document.currentScript ||
    (() => {
      const scripts = document.getElementsByTagName("script");
      return scripts[scripts.length - 1];
    })();

  const id =
    scriptTag.id ||
    (() => {
      const src = scriptTag.src;
      const url = new URL(src);
      return url.searchParams.get("id");
    })();
  iav.sendRequest = function (props) {
    const payload = JSON.stringify({ ...props, id: id, tf: "tr" });
    const trackingURL = "https://t.webmetic.de/tr";

    fetch(trackingURL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: payload,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error();
        }
        return response.json();
      })
      .then(() => {})
      .catch(() => {
        if (typeof props.eventValue === "object") {
          props.eventValue = JSON.stringify(props.eventValue);
        }
        props.tf = "png";
        var baseURL = "https://t.webmetic.de/d.png";
        var trackingURL = new URL(baseURL);

        var params = new URLSearchParams(props);
        trackingURL.search = params.toString();

        var img = new Image();
        img.src = trackingURL.href;
      });
  };
  iav.generateImg = function () {
    return Math.round(2147483647 * Math.random()).toString();
  };

  var maxScrollDepthReached = 0;
  function getScrollDepth() {
    var scrollY = "scrollY" in window ? window.scrollY : window.pageYOffset;
    var viewportHeight =
      "innerHeight" in window
        ? window.innerHeight
        : document.documentElement.clientHeight;

    return document.body
      ? Math.floor(
          ((scrollY + viewportHeight) / document.body.scrollHeight) * 100
        )
      : 0;
  }
  function updateMaxScrollDepth() {
    var currentScrollDepth = getScrollDepth();
    if (currentScrollDepth > maxScrollDepthReached) {
      maxScrollDepthReached = currentScrollDepth;
    }
  }

  function debounce(func, delay) {
    let debounceTimer;
    return function () {
      const context = this;
      const args = arguments;
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => func.apply(context, args), delay);
    };
  }
  function handleInputEvent(event) {
    var iE = event.target;
    var iV = iE.value.trim();
    var dR =
      /\b(?:http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?([a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5})(?:\/|$)/i;
    var eR = /@([\w.-]+\.[a-zA-Z]{2,6})$/i;
    var eM = iV.match(eR);
    var dM = eM ? null : iV.match(dR);
    var d = dM ? dM[1] : null;
    var e = eM ? eM[1] : null;
    if (d || e) {
      var iED = {
        event_name: d ? "doInput" : "emInput",
        event_value: d || e,
        elementClass: iE.className,
        parentElementInfo: `${iE.parentElement.tagName}#${iE.parentElement.id}`,
        xpath: getXPathForElement(iE),
        viewportX: iE.getBoundingClientRect().left,
        viewportY: iE.getBoundingClientRect().top,
      };
      iav.sendEvent(iED.e_n, iED);
    }
  }

  window.addEventListener("load", function () {
    document.addEventListener("click", handleClickEvent);
    document.addEventListener("touchend", handleClickEvent);

    const inputs = document.getElementsByTagName("input");
    for (let i = 0; i < inputs.length; i++) {
      inputs[i].addEventListener("blur", debounce(handleInputEvent, 200));
      inputs[i].addEventListener("change", debounce(handleInputEvent, 200));
      inputs[i].addEventListener("touchend", debounce(handleInputEvent, 200));
    }

    var scrollStopTimer = null;
    var throttleTime = 250;
    function sendMaxScrollDepth() {
      var scrollDepthDetails = {
        eventScroll: "maxScrollDepth",
        sde: maxScrollDepthReached,
        bu: window.location.origin,
        dl: document.location.href,
        ua: navigator.userAgent,
        sr: `${screen.width}x${screen.height}`,
      };
      iav.sendRequest(scrollDepthDetails);
    }

    function handleScroll() {
      updateMaxScrollDepth();
      if (scrollStopTimer) {
        clearTimeout(scrollStopTimer);
      }
      scrollStopTimer = setTimeout(sendMaxScrollDepth, throttleTime);
    }

    window.addEventListener("scroll", handleScroll);
    prepareTrackingData("page_load");
  });

  function prepareTrackingData(eventType, additionalData) {
    additionalData = additionalData || {};
    var props = {
      v: 1,
      aid: id,
      t: eventType,
      bu: window.location.origin,
      ul: window.navigator.userLanguage || window.navigator.language,
      cd: screen.colorDepth + "-bit",
      sr: screen.width + "x" + screen.height,
      de: document.characterSet,
      dl: document.location.href,
      dt: document.title,
      dr: document.referrer,
      ua: navigator.userAgent,
      ep: document.location.pathname,
      vp: window.innerWidth + "x" + window.innerHeight,
      ce: navigator.cookieEnabled,
      ct: navigator.connection ? navigator.connection.effectiveType : "unknown",
      sd: getScrollDepth(),
      cs:
        window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches
          ? "dark"
          : "light",
      pl: navigator.platform || "Unknown",
    };

    for (var key in additionalData) {
      if (additionalData.hasOwnProperty(key)) {
        props[key] = additionalData[key];
      }
    }

    if (props.eventValue === "" || typeof props.eventValue === "undefined") {
      delete props.eventValue;
    }

    if (props.link_url === "" || typeof props.link_url === "undefined") {
      delete props.link_url;
    }
    iav.sendRequest(props);
  }

  iav.sendEvent = function (name, value, link_url = "") {
    var eventDetails = {
      eventName: name,
      eventValue: value,
      link_url: link_url,
    };
    prepareTrackingData("interaction", eventDetails);
  };

  function handleClickEvent(event) {
    var clickedElement = event.target;

    var link_url =
      clickedElement.tagName.toLowerCase() === "a" ? clickedElement.href : "";
    var elementClass = clickedElement.className;
    var parentElementInfo = clickedElement.parentElement
      ? `${clickedElement.parentElement.tagName}#${clickedElement.parentElement.id}`
      : "No parent element";

    var xpath = getXPathForElement(clickedElement);
    var viewportX = clickedElement.getBoundingClientRect().left;
    var viewportY = clickedElement.getBoundingClientRect().top;

    var newEvent = {
      event_name: "click",
      event_value: `${clickedElement.tagName}#${clickedElement.id}`,
      link_url: link_url,
      elementclass: elementClass,
      parentelementinfo: parentElementInfo,
      xpath: xpath,
      viewportx: viewportX,
      viewporty: viewportY,
    };
    iav.sendEvent("click", newEvent);
  }

  document.addEventListener("focusin", function (event) {
    var focusEventDetails = {
      event_name: "focus",
      event_value: event.target.tagName + "#" + event.target.id,
      elementclass: event.target.className,
      parentelementinfo: `${event.target.parentElement.tagName}#${event.target.parentElement.id}`,
      xpath: getXPathForElement(event.target),
      viewportx: event.target.getBoundingClientRect().left,
      viewporty: event.target.getBoundingClientRect().top,
    };
    iav.sendEvent("focus", focusEventDetails);
  });
  function getXPathForElement(el) {
    var xpath = el.tagName;
    var parent = el.parentElement;
    while (parent) {
      xpath = `${parent.tagName}/${xpath}`;
      parent = parent.parentElement;
    }
    return xpath;
  }

  prepareTrackingData("page_load");
})();