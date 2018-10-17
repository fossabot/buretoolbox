/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.yetus.plugins.jenkins;

import hudson.Launcher;
import hudson.Extension;
import hudson.FilePath;
import hudson.util.FormValidation;
import hudson.model.AbstractProject;
import hudson.model.Run;
import hudson.model.TaskListener;
import hudson.tasks.Builder;
import hudson.tasks.BuildStepDescriptor;
import org.kohsuke.stapler.DataBoundConstructor;
import org.kohsuke.stapler.QueryParameter;

import javax.servlet.ServletException;
import java.io.IOException;
import jenkins.tasks.SimpleBuildStep;
import org.jenkinsci.Symbol;
import org.kohsuke.stapler.DataBoundSetter;

// Beginning of Apache Yetus requirements

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;

import hudson.util.ArgumentListBuilder;


public class YetusBuilder extends Builder implements SimpleBuildStep {

  private String yetusDir;
  private String baseDir;
  private String projectName;
  private String patchDir;

  private Boolean dockerMode;
  private Boolean jiraMode;

  private ArgumentListBuilder args = new ArgumentListBuilder();

  @DataBoundConstructor
  public YetusBuilder(String yetusdir) {
  	this.yetusDir = yetusdir;
    this.args.add(yetusDir + "/bin/test-patch");
    this.args.add("--console-urls");
    this.args.add("--jenkins");
    this.args.add("--resetrepo");
  }

  @DataBoundSetter
  public void setArchivelist(String archivelist) {
    this.args.add("--archive-list=" + archivelist);
  }

  @DataBoundSetter
  public void setBriefreportfile(String briefreportfile) {
    this.args.add("--brief-report-file=" + briefreportfile);
  }

  @DataBoundSetter
  public void setDocker(Boolean docker) {
    this.dockerMode = docker;
    if (dockerMode) {
      this.args.add("--docker");
    }
  }

  @DataBoundSetter
  public void setDockerfile(String dockerfile) {
    if (dockerMode) {
      this.args.add("--dockerfile=" + dockerfile);
    }
  }

  @DataBoundSetter
  public void setFindbugsstrictprecheck(Boolean findbugsstrictprecheck) {
    if (findbugsstrictprecheck) {
      this.args.add("--findbugs-strict-precheck");
    }
  }

  @DataBoundSetter
  public void setJira(Boolean jira) {
    this.jiraMode = jira;
  }

  @DataBoundSetter
  public void setJirapasswd(String jirapasswd) {
    if (jiraMode) {
      this.args.add("--jira-passwd=" + jirapasswd);
    }
  }

  @DataBoundSetter
  public void setJirauser(String jirauser) {
    if (jiraMode) {
      this.args.add("--jira-user=" + jirauser);
    }
  }

  @DataBoundSetter
  public void setDockermemlimit(String dockermemlimit) {
    if (dockerMode) {
      this.args.add("--dockermemlimit=" + dockermemlimit);
    }
  }

  @DataBoundSetter
  public void setProclimit(String procmemlimit) {
    this.args.add("--procmemlimit=" + procmemlimit);
  }

  @DataBoundSetter
  public void setProjectname(String projectname) {
  	this.projectName = projectname;
    this.args.add("--project=" + projectname);
  }

  @DataBoundSetter
  public void setPatchdir(String patchdir) {
    this.args.add("--patch-dir=" + patchdir);
    this.args.add("--build-url-artifacts=artifact/" + patchdir);
    this.args.add("--console-report-file=artifact/"
        + patchdir
        + "/console-report.txt");
    this.args.add("--html-report-file=artifact/"
        + patchdir
        + "/console-report.html");
  }

  @DataBoundSetter
  public void setReapermode(String reapermode) {
    if (dockerMode) {
      this.args.add("--reapermode=" + reapermode);
    }
  }

  public void enableShelldocs(String procmemlimit) {
    if (dockerMode && projectName.length() > 0) {
      this.args.add("--shelldocs=/testptch/"
        + projectName
        + "/precommit/bin/shelldocs");
    } else {
      this.args.add("--shelldocs="
        + yetusDir
        + "/bin/shelldocs");
    }
  }

  @Override
  public void perform(Run<?, ?> run,
      FilePath workspace,
      Launcher launcher,
      TaskListener listener) throws InterruptedException, IOException {

    listener.getLogger().println("basedir = " + baseDir);
    listener.getLogger().println("yetusdir = " + yetusDir);

    FilePath yetusSpace = new FilePath(workspace, yetusDir);

    yetusSpace.installIfNecessaryFrom(this.getClass()
                               .getClassLoader()
                               .getResource("yetus-bin.zip"), listener, "Yo!");

    launcher
        .launch()
        .cmds(args)
        .stdout(listener)
        .join();
  }

  @Symbol("greet")
  @Extension
  public static final class DescriptorImpl extends BuildStepDescriptor<Builder> {

    public FormValidation doCheckYetusdir(@QueryParameter String value)
            throws IOException, ServletException {
      if (value.length() == 0)
          return FormValidation.error(Messages.YetusBuilder_DescriptorImpl_errors_missingdir());
      return FormValidation.ok();
    }

    public FormValidation doCheckBasedir(@QueryParameter String value)
            throws IOException, ServletException {
      if (value.length() == 0)
          return FormValidation.error(Messages.YetusBuilder_DescriptorImpl_errors_missingdir());
      return FormValidation.ok();
    }

    public FormValidation doCheckPatchdir(@QueryParameter String value)
            throws IOException, ServletException {
      if (value.length() == 0)
          return FormValidation.error(Messages.YetusBuilder_DescriptorImpl_errors_missingdir());
      return FormValidation.ok();
    }

    @Override
    public boolean isApplicable(Class<? extends AbstractProject> aClass) {
      return true;
    }

    @Override
    public String getDisplayName() {
      return Messages.YetusBuilder_DescriptorImpl_DisplayName();
    }
  }
}
