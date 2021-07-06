//
//  Generated file. Do not edit.
//

#import "GeneratedPluginRegistrant.h"

#if __has_include(<modal_progress_hud_nsn/ModalProgressHudNsnPlugin.h>)
#import <modal_progress_hud_nsn/ModalProgressHudNsnPlugin.h>
#else
@import modal_progress_hud_nsn;
#endif

#if __has_include(<url_launcher/FLTURLLauncherPlugin.h>)
#import <url_launcher/FLTURLLauncherPlugin.h>
#else
@import url_launcher;
#endif

@implementation GeneratedPluginRegistrant

+ (void)registerWithRegistry:(NSObject<FlutterPluginRegistry>*)registry {
  [ModalProgressHudNsnPlugin registerWithRegistrar:[registry registrarForPlugin:@"ModalProgressHudNsnPlugin"]];
  [FLTURLLauncherPlugin registerWithRegistrar:[registry registrarForPlugin:@"FLTURLLauncherPlugin"]];
}

@end
