# Nanosmoke PWA — rebuilt preview

Visual starter rebuilt without the earlier ZIP. Includes 18+ entry gate, pulsing selection help, responsive unframed galleries, three full-screen scenarios, BOX PRO-to-ACID scratch and smoke, local selection, clearly marked demo chat, PWA manifest/PNG icons/service worker and Pages workflow.

Enable Settings → Pages → Source: GitHub Actions once. The workflow fetches catalogue/images/logo from nanosmoke.moscow and publishes _site. If extraction fails it does not publish an empty catalogue. Check Actions logs and import-report.json. Images retain the source background; actual transparent PNGs require verified cutouts. The icon is a temporary N mark, not an original brand logo. Original user video is not included in this rebuilt repository.

Scenarios currently select a primary catalogue item: ACID in bag, BOX PRO, ILIN LED in case. They do NOT include the previous additional accessory bundles. Real stock, AI, lead delivery and online ordering are not connected. Stock says availability must be confirmed, never invented. Age self-confirmation does not replace legal age checks by the seller. Hookah distance sale is not implemented. Confirm rights, public-advertising restrictions and delivery claims before public commercial use.

npm install && npm run build; serve _site over HTTPS. PWA installation depends on browser/platform support; iOS uses Share → Add to Home Screen. SW excludes APIs/inventory, network-first catalogue may be shown offline with an explicit connectivity warning. No personal data form or offline order queue.

No real-device/browser testing has been performed. Test mobile swipe, scratch, install, offline/update and source image identity before using as production. This is a starting preview, not a completed commerce app.
