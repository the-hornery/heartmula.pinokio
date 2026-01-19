module.exports = {
  version: "3.0",
  title: "HeartMuLa (HeartMuLaGen)",
  description: "Pinokio wrapper: installs HeartMuLa heartlib + downloads checkpoints + launches a Gradio UI for music generation.",

  menu: async (kernel, info) => {
    const installed = info.exists("env") && info.exists("ckpt");
    const running = {
      install: info.running("install.json"),
      start: info.running("start.json"),
      reset: info.running("reset.json")
    };
    const local = info.local("start.json");

    if (running.install) {
      return [{
        icon: "fa-solid fa-plug",
        text: "Installing…",
        href: "install.json"
      }];
    }

    if (!installed) {
      return [{
        icon: "fa-solid fa-plug",
        text: "Install",
        href: "install.json"
      }];
    }

    return [
      {
        icon: "fa-solid fa-rocket",
        text: running.start ? "Running…" : "Start",
        href: "start.json"
      },
      ...(local && local.url ? [{
        icon: "fa-solid fa-rocket",
        text: "Open UI",
        href: local.url
      }] : []),
      {
        icon: "fa-solid fa-plug",
        text: running.reset ? "Updating…" : "Update",
        href: "update.json"
      },
      {
        icon: "fa-solid fa-trash",
        text: running.reset ? "Resetting…" : "Reset (keeps /ckpt)",
        href: "reset.json"
      },
      {
        icon: "fa-solid fa-trash",
        text: running.reset ? "Hard Resetting…" : "Hard Reset (deletes /ckpt)",
        href: "hard_reset.json"
      }
    ];
  }
};
